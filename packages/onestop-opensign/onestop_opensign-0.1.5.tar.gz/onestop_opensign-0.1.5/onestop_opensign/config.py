"""
Copyright (c) 2024 OTB Africa. All rights reserved. <https://otbafrica.com>

Created Date: Tuesday, April 30th 2024, 9:04:46 pm
Author: OTB Africa, developers@otbafrica.com

Use of this source code is governed by the license that can be found in 
the LICENSE file or at https://developers.otbafrica.com/licenses/
"""

from config.settings.environment import env

OPENSIGN_API_BASE_URL = env.str('OPENSIGN_API_BASE_URL', 'http://opensign.localhost/v1/')
OPENSIGN_API_TOKEN = env.str('OPENSIGN_API_TOKEN', None)

