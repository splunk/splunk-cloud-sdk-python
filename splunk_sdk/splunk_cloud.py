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

from splunk_sdk.app_registry import AppRegistry
from splunk_sdk.action import ActionService
from splunk_sdk.auth.auth_manager import AuthManager
from splunk_sdk.base_client import get_client
from splunk_sdk.catalog import MetadataCatalog
from splunk_sdk.collect import CollectService
from splunk_sdk.common.context import Context
from splunk_sdk.kvstore import KVStoreAPI as KVStore
from splunk_sdk.ingest import IngestAPI
from splunk_sdk.gateway.client import Gateway
from splunk_sdk.provisioner import Provisioner
from splunk_sdk.search import SplunkSearchService as Search
from splunk_sdk.streams import DataStreamProcessingRESTAPI as Streams
from splunk_sdk.identity import Identity
from splunk_sdk.forwarders import SplunkForwarderService as Forwarders
from splunk_sdk.ml import MachineLearning


class SplunkCloud(object):
    """
    The SplunkCloud class ties all of the Splunk Cloud services together.
    Use this class to get started with the Splunk Cloud Platform.

    To create the client, provide a `Context` object with your tenant and an `AuthManager`
    object containing the appropriate app credentials.
    """

    def __init__(self, context: Context, auth_manager: AuthManager, requests_hooks=None):
        """
        Creates a new instance of the SplunkCloud class
        :param context: a Context object that configures the behavior of the client. Setting 'tenant' will be
            required in almost all circumstances
        :param auth_manager: A subclass of AuthManager that contains credentials for connecting to the Splunk Developer
            Cloud.
        """
        self.base_client = get_client(context, auth_manager, requests_hooks=requests_hooks)

        '''supported services'''
        self.action = ActionService(self.base_client)
        self.app_registry = AppRegistry(self.base_client)
        self.catalog = MetadataCatalog(self.base_client)
        self.collect = CollectService(self.base_client)
        self.forwarders = Forwarders(self.base_client)
        self.gateway = Gateway(self.base_client)
        self.identity = Identity(self.base_client)
        self.ingest = IngestAPI(self.base_client)
        self.kvstore = KVStore(self.base_client)
        self.provisioner = Provisioner(self.base_client)
        self.search = Search(self.base_client)
        self.streams = Streams(self.base_client)
        self.ml = MachineLearning(self.base_client)
