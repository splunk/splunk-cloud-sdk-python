from sdk.base_client import get_client
from sdk.kvstore.client import KVStore
from sdk.gateway.client import Gateway


class SplunkCloud(object):

    def __init__(self, context, auth_manager):
        self.base_client = get_client(context, auth_manager)
        '''supported services'''
        self.kvstore = KVStore(self.base_client)
        self.gateway = Gateway(self.base_client)
