"""
Copyright (c) 2024 OTB Africa. All rights reserved. <https://otbafrica.com>

Created Date: Tuesday, April 30th 2024, 8:26:14 pm
Author: OTB Africa, developers@otbafrica.com

Use of this source code is governed by the license that can be found in 
the LICENSE file or at https://developers.otbafrica.com/licenses/
"""

INSTALLED_APPS = [
    'onestop_opensign',
]

OS_DIGITAL_SIGNATURE_EXTENSIONS = ({
    'opensign': {
        'DIGITAL_SIGNATURE_PROVIDER_NAME': "OpenSign",
        'DIGITAL_SIGNATURE_PROVIDER_CLASS': "onestop_opensign.provider.OpenSignSignatureProvider"
    },
})
