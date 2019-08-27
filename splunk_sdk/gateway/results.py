# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class Spec(object):
    """The Spec class TODO DOCS."""

    def __init__(self, name=None, links=None):
        self._name = name
        self._links = links

        if self._links:
            self._json = links['json']
            self._yaml = links['yaml']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, links):
        self._links = links

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, json):
        self._json = json

    @property
    def yaml(self):
        return self._yaml

    @yaml.setter
    def yaml(self, yaml):
        self._yaml = yaml
