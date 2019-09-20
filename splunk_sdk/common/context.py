# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class Context(object):
    """
    A Context exists to configure the SDK's behavior. The one setting that needs to be made in almost every instance is
    defining the tenant that should be made for subsequent requests. This Context is then passed in to create a
    service instance or a SplunkCloud instance:

    Example:
        client = SplunkCloud(Context(tenant="mytenant"), authManager)
        client.identity.validate()
    """

    DEFAULT_API_HOST = "api.scp.splunk.com"
    DEFAULT_HOST = DEFAULT_API_HOST

    def __init__(self, host=DEFAULT_HOST, api_host=DEFAULT_API_HOST,
                 port=None, scheme="https", tenant='system', debug=False):
        self.host = host
        self.api_host = api_host
        self.port = port
        self.scheme = scheme
        self.tenant = tenant
        self.debug = debug
