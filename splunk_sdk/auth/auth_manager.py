# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from datetime import datetime
from abc import ABC, abstractmethod

DEFAULT_SCOPE = 'openid email profile'
DEFAULT_REFRESH_SCOPE = 'openid offline_access email profile'


class AuthContext(object):

    def __init__(self, token_type, access_token, expires_in, scope,
                 id_token=None, refresh_token=None):
        self._token_type = token_type
        self._access_token = access_token
        self._expires_in = expires_in
        self._scope = scope
        self._id_token = id_token
        self._refresh_token = refresh_token
        self._created_at = datetime.now()

    @property
    def token_type(self) -> str:
        return self._token_type

    @token_type.setter
    def token_type(self, token_type: str):
        self._token_type = token_type

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, access_token: str):
        self._access_token = access_token

    @property
    def expires_in(self) -> int:
        return self._expires_in

    @expires_in.setter
    def expires_in(self, expires_in: int):
        self._expires_in = expires_in

    @property
    def scope(self) -> str:
        return self._scope

    @scope.setter
    def scope(self, scope: str):
        self._scope = scope

    @property
    def id_token(self) -> str:
        return self._id_token

    @id_token.setter
    def id_token(self, id_token: str):
        self._id_token = id_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token: str):
        self._refresh_token = refresh_token


class AuthManager(ABC):
    """
    Base class for classes that manage different authentication flows.
    When creating an auth manager, create one of the subclasses that
    matches the flow that you need for your application.
    """

    def __init__(self, host, client_id, authn_url=None):
        self.host = host
        self.client_id = client_id
        self.authn_url = authn_url

    @abstractmethod
    def authenticate(self) -> AuthContext:
        """
        Makes the required calls to authorization endpoints and returns an
        AuthContext instance that can be used for subsequent calls to service
        endpoints.
        :return:
        """
        raise NotImplementedError

    def refresh(self):
        raise NotImplementedError


