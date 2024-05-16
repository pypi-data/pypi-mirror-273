"""
Copyright (c) 2024 OTB Africa. All rights reserved. <https://otbafrica.com>

Created Date: Tuesday, April 30th 2024, 8:28:27 pm
Author: OTB Africa, developers@otbafrica.com

Use of this source code is governed by the license that can be found in 
the LICENSE file or at https://developers.otbafrica.com/licenses/
"""

import json
import logging
import requests
from typing import List, TypedDict, Optional

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from apps.base import utils as base_utils
from apps.digital_signatures.provider import AbstractSignatureProvider
from apps.onestopauth.models import Team
from apps.onestopdocuments import utils as document_utils

from . import config
from .models import OpenSignDocumentTracker

_logger = logging.getLogger(__name__)


class OpenSignSignerWidgetOptions(TypedDict):
    required: bool
    name: str


class OpenSignSignerWidget(TypedDict):
    type: str
    page: int
    x: int
    y: int
    w: int
    h: int
    options: Optional[OpenSignSignerWidgetOptions]


class OpenSignDocumentSigner(TypedDict):
    name: str
    email: str
    phone: str
    widgets: List[OpenSignSignerWidget]


class OpenSignDocumentSignURL(TypedDict):
    email: str
    url: str


class OpenSignCreateDocumentPayload(TypedDict):
    file: str
    title: str
    description: str
    note: str
    signers: List[OpenSignDocumentSigner]


class OpenSignCreateDraftDocumentResponse(TypedDict):
    objectId: str
    url: str


class OpenSignCreateDocumentResponse(TypedDict):
    objectId: str
    message: str
    signurl: List[OpenSignDocumentSignURL]


class OpenSignAPIClient:
    api_token = config.OPENSIGN_API_TOKEN

    @property
    def base_url(self):
        base_url = config.OPENSIGN_API_BASE_URL
        return base_url if base_url.endswith('/') else f"{base_url}/"
    
    def get_endpoint(self, resource: str):
        return f"{self.base_url}{resource}"
    
    def get_create_document_data(self, base_64_document: str, title: str, signers: List[OpenSignDocumentSigner], description, note) -> OpenSignCreateDocumentPayload:
        return dict(
            file=base_64_document.decode(),
            title=title,
            description=description,
            note=note,
            signers=signers
        )

    def create_draft_document(self, base_64_document: str, title: str, signers: List[OpenSignDocumentSigner], **kwargs) -> OpenSignCreateDraftDocumentResponse:
        description = kwargs.get('description', '')
        note = kwargs.get('note', '')
        data=json.dumps(self.get_create_document_data(
            base_64_document=base_64_document,
            title=title,
            signers=signers,
            description=description,
            note=note
        ))
        response = requests.post(
            self.get_endpoint('draftdocument'),
            headers={
                'x-api-token': self.api_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            data=data
        )
        _logger.info(f"OpenSign: Response for Create Draft Document: {response.json()}\n\n")
        return response.json()

    def create_document(self, base_64_document: str, title: str, signers: List[OpenSignDocumentSigner], **kwargs) -> OpenSignCreateDocumentResponse:
        description = kwargs.get('description', '')
        note = kwargs.get('note', '')
        data=json.dumps(self.get_create_document_data(
            base_64_document=base_64_document,
            title=title,
            signers=signers,
            description=description,
            note=note
        ))

        response = requests.post(
            self.get_endpoint('createdocument'),
            headers={
                'x-api-token': self.api_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            data=data
        )
        _logger.info(f"OpenSign: Response for Create Document: {response.json()}\n\n")
        return response.json()
    
    def delete_document(self, opensign_document_id: str):
        response = requests.delete(
            self.get_endpoint(f'document/{opensign_document_id}'),
            headers={
                'x-api-token': self.api_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        _logger.info(f"OpenSign: Response for Delete Document: {response.json()}\n\n")
        return response.json()


class OpenSignSignatureProvider(AbstractSignatureProvider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_client = OpenSignAPIClient()
    
    def create_tracker(self, document, opensign_document_id, signer_urls: List[OpenSignDocumentSignURL]) -> OpenSignDocumentTracker:
        tracker = OpenSignDocumentTracker.objects.create(
            generated_document=document,
            opensign_document_id=opensign_document_id
        )
        for signer_url in signer_urls:
            tracker.signer_trackers.create(
                signer_email=signer_url.get('email'),
                signer_url=signer_url.get('url')
            )
        return tracker

    def get_tracker(self, document) -> OpenSignDocumentTracker:
        try:
            return OpenSignDocumentTracker.objects.pending().get(generated_document=document)
        except OpenSignDocumentTracker.DoesNotExist:
            pass
        return None

    def get_signer_details(self, user, digital_signature_folder) -> OpenSignDocumentSigner:
        widgets = self.get_widgets_from_settings(user, digital_signature_folder)

        if widgets: # OpenSign does not allow a user to sign unless they have widgets set, so we do not add the signer if no widgets are set for them.
            try:
                registration_profile = user.registrationprofile
                return {
                    'name': user.profile_name,
                    'email': user.email,
                    'phone': str(registration_profile.phone_number),
                    "widgets": widgets
                }
            except ObjectDoesNotExist:
                pass

        return None
    
    def get_widgets_from_settings(self, user, digital_signature_folder) -> list:
        """
        Get widgets set in the opensign settings for the task template in the workflow.
        OpenSign requires widgets to be set before a user can sign. As per documentation, the
        format for widgets is as follows:
                "widgets": [
                    {
                    "type": "signature",
                    "page": 1,
                    "x": 244,
                    "y": 71,
                    "w": 38,
                    "h": 46
                    }
                ]
        https://docs.opensignlabs.com/docs/API-docs/createdocument
        """
        widgets = []
        try:
            digital_signing_settings = digital_signature_folder.signing_task_template.digital_signing_settings
            open_sign_settings = digital_signing_settings.settings.get('open_sign', {})

            for key, value in open_sign_settings.items():
                try:
                    team = base_utils.get_object_or_none(Team, pk=key)
                    _logger.info(f"Checking if signer is in team: {team}, set for signing...")
                except Exception as e:
                    _logger.error(f"Error occurred while getting team: {e}")
                    team = None

                if user.email == key or (team and user in team.members):
                    widgets.extend(value.get('widgets', []))

        except Exception as e:
            _logger.error(f"Error occurred while getting digital signature settings: {e}")

        return widgets

    def sign_documents(self, digital_signature_folder, request, **kwargs):
        """
        Method that signs document(s) immediately with out sending to a folder
        """
        signers = list(map(lambda user: self.get_signer_details(user, digital_signature_folder), digital_signature_folder.signers.all()))
        sign_urls = []

        for document in digital_signature_folder.generateddocument_set.all():
            doc_as_b64_string, content_type, extension, file_name = document_utils.get_pdf_as_string(
                document=document,
                cnt_type='base64',
                user=request.user
            )

            tracker = self.get_tracker(document)
            if tracker and tracker.can_cancel():
                self.api_client.delete_document(tracker.opensign_document_id)
                tracker.cancel()
                tracker.save()
                tracker = None
            elif tracker:
                opensign_document_id = tracker.opensign_document_id
                sign_urls.extend(list(map(lambda signer_tracker: dict(email=signer_tracker.signer_email, url=signer_tracker.signer_url), tracker.signer_trackers.pending())))


            if tracker is None:
                response_body = self.api_client.create_document(
                    base_64_document=doc_as_b64_string,
                    title=file_name,
                    signers=signers
                )
                
                opensign_document_id = response_body.get('objectId')
                tracker = self.create_tracker(
                    document=document,
                    opensign_document_id=opensign_document_id,
                    signer_urls=response_body.get('signurl', [])
                )
                sign_urls.extend(response_body.get('signurl', []))

        filtered_sign_urls = list(filter(lambda sign_url: sign_url.get('email') == request.user.email, sign_urls))
        if filtered_sign_urls:
            sign_url = filtered_sign_urls[0].get('url')
            return JsonResponse(dict(redirect_url=sign_url))
        
        process_instance = kwargs.get('context', {}).get('process')
        messages.info(request, f"Document sent for signing with OpenSign. You are not among any of the signers.")
        return JsonResponse(dict(redirect_url=process_instance.get_absolute_url() if process_instance else ''))

    def sign_folder_documents(self, digital_signature_folder, request, **kwargs):
        return self.sign_documents(digital_signature_folder, request, **kwargs)

    def on_user_add_to_folder(self, *args, **kwargs):
        """
        Do nothing since OpenSign does not support multiple docs per signing
        """
        pass

    def on_auto_add_to_folder(self, *args, **kwargs):
        """
        Do nothing since OpenSign does not support multiple docs per signing
        """
        pass
