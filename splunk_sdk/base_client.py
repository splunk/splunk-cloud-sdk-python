# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import requests
import json
from splunk_sdk import __version__
from ast import literal_eval


class BaseClient(object):
    """Service Client wrapper around http requests Session"""

    def __init__(self, context, auth_manager):
        self.context = context
        self._session = requests.Session()
        self._session.headers.update({
            'Splunk-Client': 'client-python/{}'.format(__version__)})

        # TODO(dan): authenticate could check if token is valid/refresh later
        self.auth_context = auth_manager.authenticate()

        if self.auth_context:
            self._session.headers.update({
                'Authorization': "Bearer %s" % self.auth_context.access_token})

    def get(self, url, **kwargs):
        # Params are used for querystring vars
        return self._session.get(url, params=kwargs)

    def options(self, url, **kwargs):
        return self._session.options(url, **kwargs)

    def head(self, url, **kwargs):
        return self._session.head(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self._session.post(url, data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self._session.put(url, data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self._session.patch(url, data, **kwargs)

    def delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    def build_url(self, route, **kwargs):
        """Return a string url"""
        url = self.context.scheme + "://" + self.context.host
        if self.context.port is not None and self.context.port != "":
            url += ":" + self.context.port

        # TODO: all services should migrate to this pattern so tenant is
        # only set in one place
        if "{tenant}" not in url and 'omit_tenant' not in kwargs:
            url += "/" + self.get_tenant()
        url += route

        # set any url path vars
        if len(kwargs) > 0:
            url = url.format(**kwargs)

        return url

    def get_tenant(self):
        return self.context.tenant


def get_client(context, auth_manager):
    """Return a Service Client for a given auth manager"""
    return BaseClient(context, auth_manager)


# TODO: refactor this helper away and make handle_resposne cleaner
def _handle_list_response(collection, klass):
    return [klass(**e) for e in collection]


def handle_response(response, klass, key=None):
    if 200 <= response.status_code < 300:
        data = json.loads(response.text)

        # TODO(dan): dict of dict

        if klass is object:
            return data

        # Top level JSON array or object
        if key is None:
            if isinstance(data, list):
                return _handle_list_response(data, klass)
            return klass(**data)

        # Get specific key from dict containing a list
        if key is not None:
            collection = data[key]
            if isinstance(collection, list):
                return _handle_list_response(collection, klass)

        raise Exception("Unexpected http response body: {}".format(data))

    else:
        raise HTTPError(response.status_code, response.text)


class HTTPError(Exception):
    """Exception wrapper for HTTP Error responses"""

    def __init__(self, httpStatusCode, details):
        self._http_status_code = httpStatusCode
        self._http_details = details
        self._code = literal_eval(self._http_details)['code']
        self._details = literal_eval(self._http_details)['details']
        self._message = literal_eval(self._http_details)['message']

    @property
    def httpStatusCode(self):
        return self._http_status_code

    @httpStatusCode.setter
    def query(self, httpStatusCode):
        self._http_status_code = httpStatusCode

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, details):
        self._details = details

    @property
    def code(self):
        return self._code

    @property
    def details(self):
        return self._details

    @property
    def message(self):
        return self._message
