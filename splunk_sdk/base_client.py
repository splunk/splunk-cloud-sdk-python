import requests
import json
from splunk_sdk import __version__


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
        return self._session.get(url, **kwargs)

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


def handle_response(response, klass, key=None):
    if response.status_code >= 200 and response.status_code < 300:
        data = json.loads(response.text)

        # TODO(dan): list
        # TODO(dan): dict of dict

        # dict represents an obj
        if key is None:
            return klass(**data)

        # dict containing a list
        if key is not None:
            collection = data[key]
            if isinstance(collection, list):
                return [klass(**e) for e in collection]

    else:
        raise Exception("Unhandled http response code:{}".format(
            response.status_code))
