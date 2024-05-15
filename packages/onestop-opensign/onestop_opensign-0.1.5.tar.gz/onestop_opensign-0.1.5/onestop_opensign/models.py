"""
Copyright (c) 2024 OTB Africa. All rights reserved. <https://otbafrica.com>

Created Date: Sunday, May 5th 2024, 8:00:41 pm
Author: OTB Africa, developers@otbafrica.com

Use of this source code is governed by the license that can be found in 
the LICENSE file or at https://developers.otbafrica.com/licenses/
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_fsm import transition, FSMField, can_proceed

from apps.digital_signatures.models import DigitalSignatureFolder


class OpenSignTrackerQuerySet(models.QuerySet):
    class STATUS(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        SIGNED = 'SIGNED', _('Signed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    def signed(self):
        return self.filter(status=self.STATUS.SIGNED)
    
    def pending(self):
        return self.filter(status=self.STATUS.PENDING)
    
    def cancelled(self):
        return self.filter(status=self.STATUS.CANCELLED)

class OpenSignDocumentTracker(models.Model):
    """
    Model for tracking OpenSign document. Since OpenSign does not support signing multiple
    documents at once, we cannot effectively use the digital signing folder to sync the status
    between opensign and onestop.
    """

    generated_document = models.ForeignKey('onestopdocuments.GeneratedDocument', on_delete=models.CASCADE)
    opensign_document_id = models.CharField(max_length=255)
    status = FSMField(max_length=20, choices=OpenSignTrackerQuerySet.STATUS.choices, default=OpenSignTrackerQuerySet.STATUS.PENDING)

    objects = OpenSignTrackerQuerySet.as_manager()

    class Meta:
        db_table = 'opensign_document_tracker'
        unique_together = ('generated_document', 'opensign_document_id', 'status')
    
    @transition(field=status, source=OpenSignTrackerQuerySet.STATUS.PENDING, target=OpenSignTrackerQuerySet.STATUS.SIGNED)
    def mark_as_signed(self):
        self.status = OpenSignTrackerQuerySet.STATUS.SIGNED
    
    def _cancellation_check(self) -> bool:
        digital_signature_folder: DigitalSignatureFolder = self.generated_document.digital_signature_folder
        folder_is_good_to_go = digital_signature_folder and digital_signature_folder.status in [
            digital_signature_folder.SIGNING_FOLDER_STATUS_CHOICES.pending,
            digital_signature_folder.SIGNING_FOLDER_STATUS_CHOICES.processing,
        ]
        no_one_has_signed = not self.signer_trackers.signed().exists()
        return folder_is_good_to_go and no_one_has_signed

    @transition(field=status, source=OpenSignTrackerQuerySet.STATUS.PENDING, target=OpenSignTrackerQuerySet.STATUS.CANCELLED, conditions=[_cancellation_check])
    def cancel(self):
        self.status = OpenSignTrackerQuerySet.STATUS.CANCELLED
        for signing_tracker in self.signer_trackers.all():
            signing_tracker.cancel()
            signing_tracker.save()

    def can_cancel(self) -> bool:
        return can_proceed(self.cancel)

    @property
    def has_signed(self):
        return self.status == OpenSignTrackerQuerySet.STATUS.SIGNED


class OpenSignSignerTracker(models.Model):
    
    document_tracker = models.ForeignKey(OpenSignDocumentTracker, on_delete=models.CASCADE, related_name='signer_trackers')
    signer_email = models.EmailField()
    signer_url = models.URLField()
    status = FSMField(max_length=20, choices=OpenSignTrackerQuerySet.STATUS.choices, default=OpenSignTrackerQuerySet.STATUS.PENDING)

    objects = OpenSignTrackerQuerySet.as_manager()

    class Meta:
        db_table = 'opensign_signer_tracker'
        unique_together = ('document_tracker', 'signer_email')

    @transition(field=status, source=OpenSignTrackerQuerySet.STATUS.PENDING, target=OpenSignTrackerQuerySet.STATUS.SIGNED)
    def mark_as_signed(self):
        self.status = OpenSignTrackerQuerySet.STATUS.SIGNED
    
    @transition(field=status, source=OpenSignTrackerQuerySet.STATUS.PENDING, target=OpenSignTrackerQuerySet.STATUS.CANCELLED)
    def cancel(self):
        self.status = OpenSignTrackerQuerySet.STATUS.CANCELLED
