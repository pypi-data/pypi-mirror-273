"""
Copyright (c) 2024 OTB Africa. All rights reserved. <https://otbafrica.com>

Created Date: Thursday, May 2nd 2024, 7:40:29 am
Author: OTB Africa, developers@otbafrica.com

Use of this source code is governed by the license that can be found in 
the LICENSE file or at https://developers.otbafrica.com/licenses/
"""

from functools import reduce
import logging
import requests

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.base.middleware.login import login_exempt
from apps.digital_signatures.models import DigitalSignatureFolder
from apps.onestopauth.users import get_user_model
from apps.onestopdocuments import utils as document_utils
from .models import OpenSignDocumentTracker

UserModel = get_user_model()


_logger = logging.getLogger(__name__)

@method_decorator(login_exempt, name='dispatch')
class OpenSignSignatureCallbackView(APIView):

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            _logger.error(f"Error occurred in OpenSignSignatureCallbackView: {e}")
            return Response(dict(status='error', message='An error occurred'))

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            document_tracker = OpenSignDocumentTracker.objects.get(opensign_document_id=data.get('objectId'))
            onestop_document = document_tracker.generated_document
            digital_signature_folder: DigitalSignatureFolder = onestop_document.digital_signature_folder
        except OpenSignDocumentTracker.DoesNotExist:
            _logger.error(f"Document not found for OpenSign ID: {data.get('objectId')}")
            return Response(dict(status='error', message='Document not found'))

        if data.get('event') == 'signed' and (opensign_signer := data.get('signer')):
            signer_email = opensign_signer.get('email')
            signing_user = UserModel.objects.get(email=signer_email)

            if document_tracker:
                opensign_signer_tracker = document_tracker.signer_trackers.get(signer_email=signer_email)
                opensign_signer_tracker.mark_as_signed()
                opensign_signer_tracker.save()

            digital_signature_folder.start_signing_session()
            digital_signature_folder.save()

            folder_documents = digital_signature_folder.generateddocument_set.all()
            folder_document_trackers = OpenSignDocumentTracker.objects.filter(generated_document__in=folder_documents)
            pending_signer_trackers = reduce(lambda prev, curr: prev | curr, [document_tracker.signer_trackers.pending().filter(signer_email=signer_email) for document_tracker in folder_document_trackers])
            if not pending_signer_trackers.exists():
                digital_signature_folder.record_user_signature(signing_user)
                digital_signature_folder.save()

            _logger.info(f"Signer {opensign_signer} signed successfully")

        elif data.get('event') == 'completed':
            try:
                signed_file_http_response = requests.get(data.get('file'))
                document_utils.save_signed_document_from_bytes(
                    document=onestop_document,
                    signed_file_content=signed_file_http_response.content,
                    save_directory='opensign/'
                )

                if not digital_signature_folder.has_documents_pending_signature():
                    digital_signature_folder.complete_signing_session()    
                    digital_signature_folder.save()
                    document_tracker.mark_as_signed()
                    document_tracker.save()
                _logger.info(f"Document {onestop_document.document_number} signed successfully")
            except Exception as e:
                _logger.error(f"Error occurred while processing signed document: {e}")
        return Response(dict(status='ok'))

