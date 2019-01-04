class BaseService(object):

    def __init__(self, client, cluster="api"):
        self.base_client = client

        if cluster == 'app':
            self.base_client.context.host = self.base_client.context.app_host
        else:
            self.base_client.context.host = self.base_client.context.api_host
