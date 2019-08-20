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
This package defines base functionality for making requests from Splunk SDC services.
"""

import requests
import json
import logging

from requests import Response

from splunk_sdk.__version__ import __version__
from ast import literal_eval
from functools import wraps
from typing import List, Dict

from splunk_sdk.auth.auth_manager import AuthManager
from splunk_sdk.common.context import Context
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

logger = logging.getLogger(__name__)


def log_http(fn):
    """
    Decorates requests to log the request and response if debugging is enabled on the underlying client context.
    To log requests, simply set `debug=True` when creating your initial SDK context.
    :param fn:
    :return:
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
    Internal decorator for serializing and deserializing SSCModel objects.  Should not be used directly.
    :param fn:
    :return:
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
    BaseClient encapsulates conventions, authorization, and URL handling to make basic requests against SDC. For the
    most part this class is an implementation detail, but it can be used as an 'escape hatch' of sorts if some SDC
    feature is not implemented in the SDK.

    Example:
        bc = BaseClient(Context(tenant="mytenant"), authManager)
        bc.get(bc.build_url("/identity/v2/validate")) #=> HTTP response (presuming that v2 of the validate service is deployed)
    """

    def __init__(self, context: Context, auth_manager: AuthManager):
        self.context = context
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json'})
        self._session.headers.update({
            'Splunk-Client': 'client-python/{}'.format(__version__)})
        self._auth_manager = auth_manager

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
        Issues a GET request to the supplied path.  Manages auth and setting appropriate headers
        :param url:
        :param kwargs:
        :return:
        """
        self.update_auth()
        # Params are used for querystring vars
        return self._session.get(url, params=kwargs)

    @log_http
    def options(self, url: str, **kwargs) -> requests.Response:
        """
        Issues a OPTIONS request to the supplied path.  Manages auth and setting appropriate headers
        :param url:
        :param kwargs:
        :return:
        """
        self.update_auth()
        return self._session.options(url, **kwargs)

    @log_http
    def head(self, url, **kwargs) -> requests.Response:
        """
        Issues a HEAD request to the supplied path.  Manages auth and setting appropriate headers
        :param url:
        :param kwargs:
        :return:
        """
        self.update_auth()
        return self._session.head(url, **kwargs)

    @log_http
    @preprocess_body
    def post(self, url, data=None, json=None, **kwargs) -> requests.Response:
        """
        Issues a POST request to the supplied path.  Manages auth and setting appropriate headers
        :param url:
        :param data:
        :param json:
        :param kwargs:
        :return:
        """
        self.update_auth()
        return self._session.post(url, data, json, **kwargs)

    @log_http
    @preprocess_body
    def put(self, url, data=None, **kwargs) -> requests.Response:
        """
        Issues a PUT request to the supplied path.  Manages auth and setting appropriate headers
        :param url:
        :param data:
        :param kwargs:
        :return:
        """
        self.update_auth()
        return self._session.put(url, data, **kwargs)

    @log_http
    @preprocess_body
    def patch(self, url, data=None, **kwargs) -> requests.Response:
        """
        Issues a PATCH request to the supplied path.  Manages auth and setting appropriate headers
        :param url:
        :param data:
        :param kwargs:
        :return:
        """
        self.update_auth()
        return self._session.patch(url, data, **kwargs)

    @log_http
    def delete(self, url: str, **kwargs) -> requests.Response:
        """
        Issues a DELETE request to the supplied path.  Manages auth and setting appropriate headers
        :param url:
        :param kwargs:
        :return:
        """
        self.update_auth()
        return self._session.delete(url, **kwargs)

    def build_url(self, route: str, **kwargs) -> str:
        """
        build_url takes an SDC path template and adds the tenant (if the path does not start with '/system'), adds the
        configured SDC host, and then applies any kwargs to the path template, returning a full URL that can be passed
        to get/put/post/patch/delete/options/head.
        :param route:
        :param kwargs:
        :return:
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
        :return: The tenant that this client is configured with
        """
        return self.context.tenant


def inflate(data, model, is_collection: bool):
    """ Handles deserializing response from services into model objects """
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
    Serializes the model into JSON. The naming conventions for the services differ from Python naming conventions,
    so serialization involves changing from Python conventions to those defined by the services. This should be
    considered private to the SDK.
    :param obj:
    :return:
    """
    if isinstance(obj, list):
        return [dictify(i) for i in obj]
    if isinstance(obj, dict):
        return {dictify(k): dictify(v) for (k, v) in obj.items()}
    if isinstance(obj, SSCModel):
        return obj.to_dict()
    else:
        return obj


def get_client(context, auth_manager):
    """Return a Service Client for a given auth manager"""
    return BaseClient(context, auth_manager)


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
    Takes an HTTP response, and serializes into the provided class (if provided). If an error occurs, this method will
    throw.
    :param response:
    :param klass:
    :param key:
    :return:
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


class HTTPError(Exception):
    """Exception wrapper for HTTP Error responses"""

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
