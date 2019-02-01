# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.


class BaseService(object):

    def __init__(self, client, cluster="api"):
        self.base_client = client

        if cluster == 'app':
            self.base_client.context.host = self.base_client.context.app_host
        else:
            self.base_client.context.host = self.base_client.context.api_host
