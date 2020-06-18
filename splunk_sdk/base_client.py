# coding: utf-8

# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
This package defines base functionality for making requests from Splunk Cloud services.
"""

import requests
import json
import logging
import time

from requests import Response

from splunk_sdk.__version__ import __version__
from ast import literal_eval
from functools import wraps
from typing import List, Dict

from splunk_sdk.auth.auth_manager import AuthManager
from splunk_sdk.common import REQUESTS_HOOK_NAME_RESPONSE
from splunk_sdk.common.context import Context
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

logger = logging.getLogger(__name__)

"""Default retry count to be used when RetryRequests is True but no other config is supplied"""
DEFAULT_RETRY_COUNT = 10
"""Default retry interval to be used when RetryRequests is True but no other config is supplied"""
DEFAULT_RETRY_INTERVAL = 1000


def log_http(fn):
    """
    Decorates requests to log the request and response when debugging is enabled
    on the underlying client context.\n
    To log requests, set `debug=True` when creating your initial SDK context.
    :param fn: TODO DOCS
    :return: TODO DOCS
    """

    @wraps(fn)
    def _wrapper(self, *args, **kwargs):
        if not self.context.debug:
            return fn(self, *args, **kwargs)

        logger.debug("REQUEST: %s %s", args, kwargs)
        resp = fn(self, *args, **kwargs)

        logger.debug("RESPONSE: [%s] %s\n", resp.status_code,
                     resp.headers)
        if resp._content_consumed:
            logger.debug("REQUEST BODY: %s\n", resp.request.body)
            logger.debug("RESPONSE BODY: %s\n", resp.text)
        return resp

    return _wrapper


def preprocess_body(fn):
    """
    Internal decorator for serializing and deserializing SSCModel objects. Do not use this function directly.
    :param fn: TODO DOCS
    :return: TODO DOCS
    """

    @wraps(fn)
    def _wrapper(self, *args, **kwargs):
        json = kwargs.get('json', None)
        newargs = kwargs
        if json:
            newargs['json'] = dictify(json)
        return fn(self, *args, **newargs)

    return _wrapper


class BaseClient(object):
    """
    The BaseClient class encapsulates conventions, authorization, and URL handling
    to make basic requests against the Splunk Cloud Platform. You can use this class
    to access a feature that has not implemented in the SDK.\n

    Example:
        bc = BaseClient(Context(tenant="mytenant"), authManager)
        bc.get(bc.build_url("/identity/v2/validate")) #=> HTTP response (presuming that v2 of the validate service is deployed)
    """

    def __init__(self, context: Context, auth_manager: AuthManager, retry_config=None, requests_hooks=None):
        self.context = context
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json'})
        self._session.headers.update({
            'Splunk-Client': 'client-python/{}'.format(__version__)})
        self._auth_manager = auth_manager
        self._retry_config = retry_config

        self._session.hooks[REQUESTS_HOOK_NAME_RESPONSE].extend(requests_hooks or [])

    def update_auth(self):
        if self._auth_manager:
            self._session.headers.update({
                'Authorization': "Bearer %s" % self._auth_manager.context.access_token})

    @property
    def auth_manager(self) -> AuthManager:
        return self._auth_manager

    @log_http
    def get(self, url: str, **kwargs) -> requests.Response:
        """
        Issues a GET request to the specified path, manages authorization, and sets headers.
        :param url: TODO DOCS
        :param kwargs: TODO DOCS
        :return: TODO DOCS
        """

        self.update_auth()
        # Params are used for querystring vars
        response = self._session.get(url, **kwargs)

        return self.handle_error_response("GET", response, url, self._retry_config, **kwargs)

    @log_http
    def options(self, url: str, **kwargs) -> requests.Response:
        """
        Issues an OPTIONS request to the specified path, manages authorization, and sets headers.
        :param url: TODO DOCS
        :param kwargs: TODO DOCS
        :return: TODO DOCS
        """

        self.update_auth()

        response = self._session.options(url, **kwargs)

        return self.handle_error_response("OPTIONS", response, url, self._retry_config, **kwargs)

    @log_http
    def head(self, url, **kwargs) -> requests.Response:
        """
        Issues a HEAD request to the specified path, manages authorization, and sets headers.
        :param url: TODO DOCS
        :param kwargs: TODO DOCS
        :return: TODO DOCS
        """

        self.update_auth()

        response = self._session.head(url, **kwargs)

        return self.handle_error_response("HEAD", response, url, self._retry_config, **kwargs)

    @log_http
    @preprocess_body
    def post(self, url, data=None, json=None, **kwargs) -> requests.Response:
        """
        Issues a POST request to the specified path, manages authorization, and sets headers.
        :param url: TODO DOCS
        :param data: TODO DOCS
        :param json: TODO DOCS
        :param kwargs: TODO DOCS
        :return: TODO DOCS
        """

        self.update_auth()

        response = self._session.post(url, data, json, **kwargs)

        return self.handle_error_response("POST", response, url, data, json, self._retry_config, **kwargs)

    @log_http
    @preprocess_body
    def put(self, url, data=None, **kwargs) -> requests.Response:
        """
        Issues a PUT request to the specified path, manages authorization, and sets headers.
        :param url: TODO DOCS
        :param data: TODO DOCS
        :param kwargs: TODO DOCS
        :return: TODO DOCS
        """

        self.update_auth()

        response = self._session.put(url, data, **kwargs)

        return self.handle_error_response("PUT", response, url, data, self._retry_config, **kwargs)

    @log_http
    @preprocess_body
    def patch(self, url, data=None, **kwargs) -> requests.Response:
        """
        Issues a PATCH request to the specified path, manages authorization, and sets headers.
        :param url:
        :param data:
        :param kwargs:
        :return:
        """

        self.update_auth()

        response = self._session.patch(url, data, **kwargs)

        return self.handle_error_response("PATCH", response, url, data, self._retry_config, **kwargs)

    @log_http
    def delete(self, url: str, **kwargs) -> requests.Response:
        """
        Issues a DELETE request to the specified path, manages authorization, and sets headers.
        :param url: TODO DOCS
        :param kwargs: TODO DOCS
        :return: TODO DOCS
        """
        self.update_auth()

        response = self._session.delete(url, **kwargs)

        return self.handle_error_response("DELETE", response, url, self._retry_config, **kwargs)

    def build_url(self, route: str, **kwargs) -> str:
        """
        Builds a full URL from the specified path template by adding the current
        tenant (if the path does not start with '/system') and the configured host,
        and applying any `kwargs` to the path template. \n
        You can pass the returned URL to GET, PUT, POST, PATCH, DELETE, OPTIONS,
        and HEAD requests.
        :param route: TODO DOCS
        :param kwargs: TODO DOCS
        :return: The full URL.
        """
        url = self.context.scheme + "://" + self.context.host
        if self.context.port is not None and self.context.port != "":
            url += ":" + self.context.port

        omit_tenant = kwargs.get("omit_tenant", False)

        if route.startswith("/system/") is False and omit_tenant is False:
            url += "/" + self.get_tenant()
        url += route

        # set any url path vars
        if len(kwargs) > 0:
            url = url.format(**kwargs)
        return url

    def get_tenant(self) -> str:
        """
        Gets the tenant for the current client.
        :return: The tenant name.
        """
        return self.context.tenant

    def handle_error_response(self, method: str, response: Response, url, data=None, json_data=None, retry_config=None, **kwargs) -> requests.Response:

        if response.status_code != 429 or retry_config is None or (retry_config is not None and retry_config.retry_requests_enabled is not True):
            return response

        retry_count = 0
        success_response = self._retry_config.handle_response(self, method, url, retry_count, data, json_data, **kwargs)
        while (success_response is not None and success_response.status_code == 429) and retry_count < self._retry_config.retry_count:
            retry_count += 1
            success_response = self._retry_config.handle_response(self, method, url, retry_count, data, json_data, **kwargs)
            if success_response is not None and success_response.status_code != 429:
                response = success_response

        return response

def inflate(data, model, is_collection: bool):
    """ Handles deserializing responses from services into model objects."""
    if data is None:
        return None
    if model is not None and hasattr(model, '_from_dict'):
        if is_collection:
            if isinstance(data, list):
                return [model._from_dict(d) for d in data]
            if isinstance(data, dict):
                return {k: model._from_dict(v) for (k, v) in data.items()}
        else:
            return model._from_dict(data)
    else:
        return data


def dictify(obj):
    """
    Private. Serializes the model into JSON. The naming conventions for the services
    differ from Python naming conventions, so serialization involves changing from
    Python conventions to those defined by the Splunk Cloud services.
    :param obj: TODO DOCS
    :return: TODO DOCS
    """
    if isinstance(obj, list):
        return [dictify(i) for i in obj]
    if isinstance(obj, dict):
        return {dictify(k): dictify(v) for (k, v) in obj.items()}
    if isinstance(obj, SSCModel):
        return obj.to_dict()
    else:
        return obj


def get_client(context, auth_manager, retry_config=None, requests_hooks=None):
    """Returns a Service Client object for the specified authorization manager."""
    client = BaseClient(context, auth_manager, retry_config=retry_config, requests_hooks=requests_hooks)
    client.update_auth()
    return client


# TODO: refactor this helper away and make handle_response cleaner
def _handle_list_response(collection, klass, response: Response):
    return [_instantiate_obj(klass, e, response) for e in collection]


def _instantiate_obj(klass, data, response: Response):
    if type(data) == dict:
        if getattr(klass, "_from_dict", None):
            instance = klass._from_dict(data)
            instance.response = response
            return instance
        else:
            return klass(**data)
    else:
        return data


def handle_response(response: Response, klass=None, key=None):
    """
    Takes an HTTP response and serializes into the provided class.
    :param response: TODO DOCS
    :param klass: TODO DOCS
    :param key: TODO DOCS
    :return: TODO DOCS
    """
    if 200 <= response.status_code < 300:
        # When we don't expect a response
        if klass is None or not response.text:
            return SSCVoidModel(response)

        data = json.loads(response.text)

        # if the klass is a primitive just return the data
        # TODO(dan): find a cleaner way to check for
        #  maybe hasattr _from_dict or _to_dict
        if klass in (object, str, List, Dict):
            return data

        # Top level JSON array or object
        if key is None:
            if isinstance(data, list):
                return _handle_list_response(data, klass, response)
            return _instantiate_obj(klass, data, response)

        # Get specific key from dict containing a list
        if key is not None:
            collection = data[key]
            if isinstance(collection, list):
                return _handle_list_response(collection, klass, response)

        raise Exception("Unexpected http response body: {}".format(data))

    else:
        raise HTTPError(response.status_code, response.text)


class RetryConfig(object):
    """The RetryConfig class wraps around the configuration values for retrying requests that fail
    when a 429 is encountered at the server."""

    def __init__(self, retry_requests_enabled: bool, retry_count=None, retry_interval=None):
        self._retry_requests_enabled = retry_requests_enabled
        if retry_count is not None:
            self._retry_count = retry_count
        else:
            self._retry_count = DEFAULT_RETRY_COUNT

        if retry_interval is not None:
            self._retry_interval = retry_interval
        else:
            self._retry_interval = DEFAULT_RETRY_INTERVAL

    @property
    def retry_requests_enabled(self) -> bool:
        return self._retry_requests_enabled

    @retry_requests_enabled.setter
    def retry_requests_enabled(self, retry_requests_enabled: bool):
        self._retry_requests_enabled = retry_requests_enabled

    @property
    def retry_count(self) -> int:
        return self._retry_count

    @retry_count.setter
    def retry_count(self, retry_count: int):
        self._retry_count = retry_count

    @property
    def retry_interval(self) -> bool:
        return self._retry_interval

    @retry_interval.setter
    def retry_interval(self, retry_interval: bool):
        self._retry_interval = retry_interval

    # implement exponential back off by increasing the waiting time between retries after each retry failure.
    def handle_response(self, client, method, url, retry_count, data=None, json_data=None, **kwargs) -> requests.Response:
        response = None
        backOffSeconds = ((1 << retry_count) * self._retry_interval) / 1000
        time.sleep(backOffSeconds)

        if method == "POST":
            response = client._session.post(url, data, json_data, **kwargs)
        elif method == "GET":
            response = self._session.get(url, **kwargs)
        elif method == "DELETE":
            response = self._session.delete(url, **kwargs)
        elif method == "OPTIONS":
            response = self._session.options(url, **kwargs)
        elif method == "HEAD":
            response = self._session.head(url, **kwargs)
        elif method == "PUT":
            response = self._session.put(url, data, **kwargs)
        elif method == "PATCH":
            response = self._session.patch(url, data, **kwargs)

        return response

class HTTPError(Exception):
    """The HTTPError class provides an exception wrapper for HTTP error responses."""

    def __init__(self, http_status_code: int, details: str):
        self._http_status_code = http_status_code
        self._http_details = details
        if details != '':
            parsed = json.loads(details)
        else:
            parsed = dict()
        self._code = parsed.get('code', 999)
        self._details = parsed.get('details', '')
        self._message = parsed.get('message', '')

    @property
    def http_status_code(self) -> int:
        return self._http_status_code

    @http_status_code.setter
    def http_status_code(self, http_status_code: int):
        self._http_status_code = http_status_code

    @property
    def details(self) -> str:
        return self._details

    @details.setter
    def details(self, details: str):
        self._details = details

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self):
        return self._message
