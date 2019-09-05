# Copyright © 2019 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# [http://www.apache.org/licenses/LICENSE-2.0]
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

############# This file is auto-generated.  Do not edit! #############

"""
    SDC Service: KV Store API

    With the Splunk Cloud KV store service, you can save and retrieve data within your Splunk apps, enabling you to manage and maintain the state of the application.

    OpenAPI spec version: v1beta1.2 (recommended default)
    Generated by: https://openapi-generator.tech
"""


from datetime import datetime
from typing import List, Dict
from splunk_sdk.common.sscmodel import SSCModel
from splunk_sdk.base_client import dictify, inflate
from enum import Enum



class ErrorResponse(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "ErrorResponse":
        instance = ErrorResponse.__new__(ErrorResponse)
        instance._attrs = model
        return instance

    def __init__(self, code: "str", message: "str", **extra):
        """ErrorResponse"""

        self._attrs = dict()
        if code is not None:
            self._attrs["code"] = code
        if message is not None:
            self._attrs["message"] = message
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def code(self) -> "str":
        """ Gets the code of this ErrorResponse.
        Internal status code of the error.
        """
        return self._attrs.get("code")

    @code.setter
    def code(self, code: "str"):
        """Sets the code of this ErrorResponse.

        Internal status code of the error.

        :param code: The code of this ErrorResponse.
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")
        self._attrs["code"] = code

    @property
    def message(self) -> "str":
        """ Gets the message of this ErrorResponse.
        Detailed error message.
        """
        return self._attrs.get("message")

    @message.setter
    def message(self, message: "str"):
        """Sets the message of this ErrorResponse.

        Detailed error message.

        :param message: The message of this ErrorResponse.
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")
        self._attrs["message"] = message

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class IndexFieldDefinition(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "IndexFieldDefinition":
        instance = IndexFieldDefinition.__new__(IndexFieldDefinition)
        instance._attrs = model
        return instance

    def __init__(self, direction: "int", field: "str", **extra):
        """IndexFieldDefinition"""

        self._attrs = dict()
        if direction is not None:
            self._attrs["direction"] = direction
        if field is not None:
            self._attrs["field"] = field
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def direction(self) -> "int":
        """ Gets the direction of this IndexFieldDefinition.
        The sort direction for the indexed field.
        """
        return self._attrs.get("direction")

    @direction.setter
    def direction(self, direction: "int"):
        """Sets the direction of this IndexFieldDefinition.

        The sort direction for the indexed field.

        :param direction: The direction of this IndexFieldDefinition.
        :type: int
        """
        if direction is None:
            raise ValueError("Invalid value for `direction`, must not be `None`")
        self._attrs["direction"] = direction

    @property
    def field(self) -> "str":
        """ Gets the field of this IndexFieldDefinition.
        The name of the field to index.
        """
        return self._attrs.get("field")

    @field.setter
    def field(self, field: "str"):
        """Sets the field of this IndexFieldDefinition.

        The name of the field to index.

        :param field: The field of this IndexFieldDefinition.
        :type: str
        """
        if field is None:
            raise ValueError("Invalid value for `field`, must not be `None`")
        self._attrs["field"] = field

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class IndexDefinition(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "IndexDefinition":
        instance = IndexDefinition.__new__(IndexDefinition)
        instance._attrs = model
        return instance

    def __init__(self, fields: "List[IndexFieldDefinition]", name: "str", **extra):
        """IndexDefinition"""

        self._attrs = dict()
        if fields is not None:
            self._attrs["fields"] = fields
        if name is not None:
            self._attrs["name"] = name
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def fields(self) -> "List[IndexFieldDefinition]":
        """ Gets the fields of this IndexDefinition.
        """
        return [IndexFieldDefinition._from_dict(i) for i in self._attrs.get("fields")]

    @fields.setter
    def fields(self, fields: "List[IndexFieldDefinition]"):
        """Sets the fields of this IndexDefinition.


        :param fields: The fields of this IndexDefinition.
        :type: List[IndexFieldDefinition]
        """
        if fields is None:
            raise ValueError("Invalid value for `fields`, must not be `None`")
        self._attrs["fields"] = fields

    @property
    def name(self) -> "str":
        """ Gets the name of this IndexDefinition.
        The name of the index.
        """
        return self._attrs.get("name")

    @name.setter
    def name(self, name: "str"):
        """Sets the name of this IndexDefinition.

        The name of the index.

        :param name: The name of this IndexDefinition.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        self._attrs["name"] = name

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class IndexDescription(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "IndexDescription":
        instance = IndexDescription.__new__(IndexDescription)
        instance._attrs = model
        return instance

    def __init__(self, collection: "str" = None, fields: "List[IndexFieldDefinition]" = None, name: "str" = None, **extra):
        """IndexDescription"""

        self._attrs = dict()
        if collection is not None:
            self._attrs["collection"] = collection
        if fields is not None:
            self._attrs["fields"] = fields
        if name is not None:
            self._attrs["name"] = name
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def collection(self) -> "str":
        """ Gets the collection of this IndexDescription.
        The collection name.
        """
        return self._attrs.get("collection")

    @collection.setter
    def collection(self, collection: "str"):
        """Sets the collection of this IndexDescription.

        The collection name.

        :param collection: The collection of this IndexDescription.
        :type: str
        """
        self._attrs["collection"] = collection

    @property
    def fields(self) -> "List[IndexFieldDefinition]":
        """ Gets the fields of this IndexDescription.
        """
        return [IndexFieldDefinition._from_dict(i) for i in self._attrs.get("fields")]

    @fields.setter
    def fields(self, fields: "List[IndexFieldDefinition]"):
        """Sets the fields of this IndexDescription.


        :param fields: The fields of this IndexDescription.
        :type: List[IndexFieldDefinition]
        """
        self._attrs["fields"] = fields

    @property
    def name(self) -> "str":
        """ Gets the name of this IndexDescription.
        The name of the index.
        """
        return self._attrs.get("name")

    @name.setter
    def name(self, name: "str"):
        """Sets the name of this IndexDescription.

        The name of the index.

        :param name: The name of this IndexDescription.
        :type: str
        """
        self._attrs["name"] = name

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class Key(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "Key":
        instance = Key.__new__(Key)
        instance._attrs = model
        return instance

    def __init__(self, key: "str", **extra):
        """Key"""

        self._attrs = dict()
        if key is not None:
            self._attrs["_key"] = key
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def key(self) -> "str":
        """ Gets the key of this Key.
        Key of the inserted document.
        """
        return self._attrs.get("_key")

    @key.setter
    def key(self, key: "str"):
        """Sets the key of this Key.

        Key of the inserted document.

        :param key: The key of this Key.
        :type: str
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")
        self._attrs["_key"] = key

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class StatusEnum(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

    @staticmethod
    def from_value(value: str):
        if value == "healthy":
            return StatusEnum.HEALTHY
        if value == "unhealthy":
            return StatusEnum.UNHEALTHY
        if value == "unknown":
            return StatusEnum.UNKNOWN


class PingResponse(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "PingResponse":
        instance = PingResponse.__new__(PingResponse)
        instance._attrs = model
        return instance

    def __init__(self, status: "str", error_message: "str" = None, **extra):
        """PingResponse"""

        self._attrs = dict()
        if status is not None:
            self._attrs["status"] = status
        if error_message is not None:
            self._attrs["errorMessage"] = error_message
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def status(self) -> "StatusEnum":
        """ Gets the status of this PingResponse.
        Database status.
        """
        return StatusEnum.from_value(self._attrs.get("status"))

    @status.setter
    def status(self, status: "str"):
        """Sets the status of this PingResponse.

        Database status.

        :param status: The status of this PingResponse.
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")
        if isinstance(status, Enum):
            self._attrs["status"] = status.value
        else:
            self._attrs["status"] = status  # If you supply a string, we presume you know the service will take it.

    @property
    def error_message(self) -> "str":
        """ Gets the error_message of this PingResponse.
        If database is not healthy, detailed error message.
        """
        return self._attrs.get("errorMessage")

    @error_message.setter
    def error_message(self, error_message: "str"):
        """Sets the error_message of this PingResponse.

        If database is not healthy, detailed error message.

        :param error_message: The error_message of this PingResponse.
        :type: str
        """
        self._attrs["errorMessage"] = error_message

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}
