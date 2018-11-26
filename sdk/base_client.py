import requests
import json


class BaseClient(object):
    """Service Client wrapper around http requests Session"""

    def __init__(self, context, token):
        self.context = context
        # TODO(dan): may want to use session conditionally, leaves sockets open
        self._session = requests.Session()
        # TODO(dan): read from version
        self._session.headers.update({'Splunk-Client': 'client-python/0.0.1'})

        if token:
            self._session.headers.update({
                'Authorization': "Bearer %s" % token})

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
    """Return a Service Client for a given auth method"""
    auth_context = auth_manager.authenticate()
    return BaseClient(context, token=auth_context.access_token)


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
