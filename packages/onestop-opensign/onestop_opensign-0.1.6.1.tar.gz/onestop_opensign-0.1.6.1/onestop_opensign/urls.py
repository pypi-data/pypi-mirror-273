"""
Copyright (c) 2024 OTB Africa. All rights reserved. <https://otbafrica.com>

Created Date: Thursday, May 2nd 2024, 7:40:56 am
Author: OTB Africa, developers@otbafrica.com

Use of this source code is governed by the license that can be found in 
the LICENSE file or at https://developers.otbafrica.com/licenses/
"""

from django.urls import path

from .views import OpenSignSignatureCallbackView


urlpatterns = [
    path('TkuZhGCITH/', OpenSignSignatureCallbackView.as_view(), name='opensign-signature-callback')
]
