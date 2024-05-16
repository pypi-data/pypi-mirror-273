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

from typing import Any, Optional
from typing_extensions import Self

class VipasException(Exception):
    """The base exception class for all VipasExceptions"""

class ClientException(VipasException):

    def __init__(
        self, 
        status=None, 
        reason=None, 
        http_resp=None,
        *,
        body: Optional[str] = None,
        data: Optional[Any] = None,
    ) -> None:
        self.status = status
        self.reason = reason
        self.body = body
        self.data = data
        self.headers = None

        if http_resp:
            if self.status is None:
                self.status = http_resp.status
            if self.reason is None:
                self.reason = http_resp.reason
            if self.body is None:
                try:
                    self.body = http_resp.data.decode('utf-8')
                except Exception:
                    pass
            self.headers = http_resp.getheaders()

    @classmethod
    def from_response(
        cls, 
        *, 
        http_resp, 
        body: Optional[str],
        data: Optional[Any],
    ) -> Self:
        if http_resp.status_code == 400:
            raise BadRequestException(status=http_resp.status_code, reason=http_resp.reason, http_resp=http_resp, body=body, data=data)

        if http_resp.status_code == 401:
            raise UnauthorizedException(status=http_resp.status_code, reason=http_resp.reason, http_resp=http_resp, body=body, data=data)

        if http_resp.status_code == 403:
            raise ForbiddenException(status=http_resp.status_code, reason=http_resp.reason, http_resp=http_resp, body=body, data=data)

        if http_resp.status_code == 404:
            raise NotFoundException(status=http_resp.status_code, reason=http_resp.reason, http_resp=http_resp, body=body, data=data)

        if 500 <= http_resp.status_code <= 599:
            raise ConnectionException(status=http_resp.status_code, reason=http_resp.reason, http_resp=http_resp, body=body, data=data)
        raise ClientException(status=http_resp.status_code, reason=http_resp.reason, http_resp=http_resp, body=body, data=data)

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(
                self.headers)

        if self.data or self.body:
            error_message += "HTTP response body: {0}\n".format(self.data or self.body)

        return error_message


class BadRequestException(ClientException):
    pass


class NotFoundException(ClientException):
    pass


class UnauthorizedException(ClientException):
    pass


class ForbiddenException(ClientException):
    pass


class ConnectionException(ClientException):
    pass
