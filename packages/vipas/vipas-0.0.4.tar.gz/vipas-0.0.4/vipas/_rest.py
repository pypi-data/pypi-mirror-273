# coding: utf-8
"""
  Copyright (c) 2024 Vipas.AI
 
  All rights reserved. This program and the accompanying materials
  are made available under the terms of a proprietary license which prohibits
  redistribution and use in any form, without the express prior written consent
  of Vipas.AI.
  
  This code is proprietary to Vipas.AI and is protected by copyright and
  other intellectual property laws. You may not modify, reproduce, perform,
  display, create derivative works from, repurpose, or distribute this code or any portion of it
  without the express prior written permission of Vipas.AI.
  
  For more information, contact Vipas.AI at legal@vipas.ai

"""  # noqa: E501
import json
import requests

from vipas.exceptions import ClientException
class RESTClientObject:

    def __init__(self, configuration) -> None:
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter()
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def request(self, method, url, headers=None, body=None):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        """
        method = method.upper()

        # Prepare headers and body for the request
        headers = headers or {}

        if body is not None:
            body = json.dumps(body)

        # Make the HTTP request using the session
        try:
            response = self.session.request(method, url, headers=headers, data=body)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ClientException.from_response(http_resp=response, body=response.text, data=None)
        except requests.exceptions.RequestException as e:
            # Handle any errors that occur while making the request
            raise ClientException(status=500, reason=str(e))
        
        return json.loads(response.content.decode('utf-8'))
