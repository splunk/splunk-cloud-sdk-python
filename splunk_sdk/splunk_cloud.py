# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from splunk_sdk.app_registry.gen_app_registry_api import AppRegistry
from splunk_sdk.action.gen_action_service_api import ActionService
from splunk_sdk.auth.auth_manager import AuthManager
from splunk_sdk.base_client import get_client
from splunk_sdk.catalog import MetadataCatalog
from splunk_sdk.common.context import Context
from splunk_sdk.kvstore.gen_kv_store_api_api import KVStoreAPI as KVStore
from splunk_sdk.ingest.gen_ingest_api_api import IngestAPI
from splunk_sdk.gateway.client import Gateway
from splunk_sdk.provisioner import Provisioner
from splunk_sdk.search.gen_splunk_search_service_api import \
    SplunkSearchService as Search
from splunk_sdk.streams.gen_data_stream_processing_rest_api_api import \
    DataStreamProcessingRESTAPI as Streams
from splunk_sdk.identity.gen_identity_and_access_control_api import \
    IdentityAndAccessControl as Identity
from splunk_sdk.forwarders.gen_splunk_forwarder_service_api import \
    SplunkForwarderService as Forwarders
from splunk_sdk.ml.gen_machine_learning_service__ml_api_api import \
    MachineLearningServiceMLAPI


class SplunkCloud(object):
    """
    SplunkCloud ties together all services provided by Splunk SDC. This is the easiest and most straightforward place to
    get starting with the Splunk Developer Cloud.

    To create the client, simply provide a Context object with your tenant supplied and an AuthManager containing the
    appropriate app credentials.
    """

    def __init__(self, context: Context, auth_manager: AuthManager):
        """
        Creates a new instance of the SplunkCloud class
        :param context: a Context object that configures the behavior of the client. Setting 'tenant' will be
            required in almost all circumstances
        :param auth_manager: A subclass of AuthManager that contains credentials for connecting to the Splunk Developer
            Cloud.
        """
        self.base_client = get_client(context, auth_manager)

        '''supported services'''
        self.action = ActionService(self.base_client)
        self.app_registry = AppRegistry(self.base_client)
        self.catalog = MetadataCatalog(self.base_client)
        self.forwarders = Forwarders(self.base_client)
        self.gateway = Gateway(self.base_client)
        self.identity = Identity(self.base_client)
        self.ingest = IngestAPI(self.base_client)
        self.kvstore = KVStore(self.base_client)
        self.provisioner = Provisioner(self.base_client)
        self.search = Search(self.base_client)
        self.streams = Streams(self.base_client)
        self.ml = MachineLearningServiceMLAPI(self.base_client)
