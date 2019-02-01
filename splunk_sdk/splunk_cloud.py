from splunk_sdk.base_client import get_client
from splunk_sdk.kvstore.client import KVStore
from splunk_sdk.gateway.client import Gateway
from splunk_sdk.search.client import Search
from splunk_sdk.ingest.client import Ingest


class SplunkCloud(object):

    def __init__(self, context, auth_manager):
        self.base_client = get_client(context, auth_manager)

        '''supported services'''
        self.kvstore = KVStore(self.base_client)
        self.gateway = Gateway(self.base_client)
        self.search = Search(self.base_client)
        self.ingest = Ingest(self.base_client)
