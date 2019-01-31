# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

class Context(object):

    DEFAULT_HOST = "api.splunkbeta.com"
    DEFAULT_APP_HOST = "api.splunkbeta.com"
    DEFAULT_API_HOST = "app.splunkbeta.com"

    def __init__(self, host=DEFAULT_HOST, api_host=DEFAULT_APP_HOST,
                 app_host=DEFAULT_API_HOST, port=None, scheme="https",
                 ssl_verify=False, tenant='system', session=False):
        self.host = host
        self.api_host = api_host
        self.app_host = app_host
        self.port = port
        self.scheme = scheme
        self.ssl_verify = ssl_verify  # TODO(dan): not currently used
        self.tenant = tenant
        self.session = session
