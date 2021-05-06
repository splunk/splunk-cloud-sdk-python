# Copyright © 2021 Splunk, Inc.
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
    SDC Service: Provisioner

    With the Provisioner service in Splunk Cloud Services, you can provision and manage tenants.

    OpenAPI spec version: v1beta1.4 (recommended default)
    Generated by: https://openapi-generator.tech
"""


from datetime import datetime
from typing import List, Dict
from splunk_sdk.common.sscmodel import SSCModel
from splunk_sdk.base_client import dictify, inflate
from enum import Enum



class Error(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "Error":
        instance = Error.__new__(Error)
        instance._attrs = model
        return instance

    def __init__(self, code: "str", message: "str", **extra):
        """Error"""

        self._attrs = dict()
        if code is not None:
            self._attrs["code"] = code
        if message is not None:
            self._attrs["message"] = message
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def code(self) -> "str":
        """ Gets the code of this Error.
        Service error code
        """
        return self._attrs.get("code")

    @code.setter
    def code(self, code: "str"):
        """Sets the code of this Error.

        Service error code

        :param code: The code of this Error.
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")
        self._attrs["code"] = code

    @property
    def message(self) -> "str":
        """ Gets the message of this Error.
        Human readable error message
        """
        return self._attrs.get("message")

    @message.setter
    def message(self, message: "str"):
        """Sets the message of this Error.

        Human readable error message

        :param message: The message of this Error.
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")
        self._attrs["message"] = message

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class InviteBody(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "InviteBody":
        instance = InviteBody.__new__(InviteBody)
        instance._attrs = model
        return instance

    def __init__(self, email: "str", comment: "str" = None, groups: "List[str]" = None, **extra):
        """InviteBody"""

        self._attrs = dict()
        if email is not None:
            self._attrs["email"] = email
        if comment is not None:
            self._attrs["comment"] = comment
        if groups is not None:
            self._attrs["groups"] = groups
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def email(self) -> "str":
        """ Gets the email of this InviteBody.
        """
        return self._attrs.get("email")

    @email.setter
    def email(self, email: "str"):
        """Sets the email of this InviteBody.


        :param email: The email of this InviteBody.
        :type: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")
        self._attrs["email"] = email

    @property
    def comment(self) -> "str":
        """ Gets the comment of this InviteBody.
        """
        return self._attrs.get("comment")

    @comment.setter
    def comment(self, comment: "str"):
        """Sets the comment of this InviteBody.


        :param comment: The comment of this InviteBody.
        :type: str
        """
        self._attrs["comment"] = comment

    @property
    def groups(self) -> "List[str]":
        """ Gets the groups of this InviteBody.
        """
        return self._attrs.get("groups")

    @groups.setter
    def groups(self, groups: "List[str]"):
        """Sets the groups of this InviteBody.


        :param groups: The groups of this InviteBody.
        :type: List[str]
        """
        self._attrs["groups"] = groups

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class InviteInfoErrorsItems(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "InviteInfoErrorsItems":
        instance = InviteInfoErrorsItems.__new__(InviteInfoErrorsItems)
        instance._attrs = model
        return instance

    def __init__(self, action: "str", code: "str", message: "str", group: "str" = None, **extra):
        """InviteInfoErrorsItems"""

        self._attrs = dict()
        if action is not None:
            self._attrs["action"] = action
        if code is not None:
            self._attrs["code"] = code
        if message is not None:
            self._attrs["message"] = message
        if group is not None:
            self._attrs["group"] = group
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def action(self) -> "str":
        """ Gets the action of this InviteInfoErrorsItems.
        """
        return self._attrs.get("action")

    @action.setter
    def action(self, action: "str"):
        """Sets the action of this InviteInfoErrorsItems.


        :param action: The action of this InviteInfoErrorsItems.
        :type: str
        """
        if action is None:
            raise ValueError("Invalid value for `action`, must not be `None`")
        self._attrs["action"] = action

    @property
    def code(self) -> "str":
        """ Gets the code of this InviteInfoErrorsItems.
        """
        return self._attrs.get("code")

    @code.setter
    def code(self, code: "str"):
        """Sets the code of this InviteInfoErrorsItems.


        :param code: The code of this InviteInfoErrorsItems.
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")
        self._attrs["code"] = code

    @property
    def message(self) -> "str":
        """ Gets the message of this InviteInfoErrorsItems.
        """
        return self._attrs.get("message")

    @message.setter
    def message(self, message: "str"):
        """Sets the message of this InviteInfoErrorsItems.


        :param message: The message of this InviteInfoErrorsItems.
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")
        self._attrs["message"] = message

    @property
    def group(self) -> "str":
        """ Gets the group of this InviteInfoErrorsItems.
        """
        return self._attrs.get("group")

    @group.setter
    def group(self, group: "str"):
        """Sets the group of this InviteInfoErrorsItems.


        :param group: The group of this InviteInfoErrorsItems.
        :type: str
        """
        self._attrs["group"] = group

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class StatusEnum(str, Enum):
    CREATED = "created"
    INVITED = "invited"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    FAILED = "failed"
    INVALID = "invalid"

    @staticmethod
    def from_value(value: str):
        if value == "created":
            return StatusEnum.CREATED
        if value == "invited":
            return StatusEnum.INVITED
        if value == "accepted":
            return StatusEnum.ACCEPTED
        if value == "rejected":
            return StatusEnum.REJECTED
        if value == "expired":
            return StatusEnum.EXPIRED
        if value == "failed":
            return StatusEnum.FAILED
        if value == "invalid":
            return StatusEnum.INVALID


class InviteInfo(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "InviteInfo":
        instance = InviteInfo.__new__(InviteInfo)
        instance._attrs = model
        return instance

    def __init__(self, comment: "str", created_at: "datetime", created_by: "str", email: "str", errors: "List[InviteInfoErrorsItems]", expires_at: "datetime", groups: "List[str]", invite_id: "str", status: "str", tenant: "str", updated_at: "datetime", updated_by: "str", **extra):
        """InviteInfo"""

        self._attrs = dict()
        if comment is not None:
            self._attrs["comment"] = comment
        if created_at is not None:
            self._attrs["createdAt"] = created_at
        if created_by is not None:
            self._attrs["createdBy"] = created_by
        if email is not None:
            self._attrs["email"] = email
        if errors is not None:
            self._attrs["errors"] = errors
        if expires_at is not None:
            self._attrs["expiresAt"] = expires_at
        if groups is not None:
            self._attrs["groups"] = groups
        if invite_id is not None:
            self._attrs["inviteID"] = invite_id
        if status is not None:
            self._attrs["status"] = status
        if tenant is not None:
            self._attrs["tenant"] = tenant
        if updated_at is not None:
            self._attrs["updatedAt"] = updated_at
        if updated_by is not None:
            self._attrs["updatedBy"] = updated_by
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def comment(self) -> "str":
        """ Gets the comment of this InviteInfo.
        """
        return self._attrs.get("comment")

    @comment.setter
    def comment(self, comment: "str"):
        """Sets the comment of this InviteInfo.


        :param comment: The comment of this InviteInfo.
        :type: str
        """
        if comment is None:
            raise ValueError("Invalid value for `comment`, must not be `None`")
        self._attrs["comment"] = comment

    @property
    def created_at(self) -> "datetime":
        """ Gets the created_at of this InviteInfo.
        """
        return self._attrs.get("createdAt")

    @created_at.setter
    def created_at(self, created_at: "datetime"):
        """Sets the created_at of this InviteInfo.


        :param created_at: The created_at of this InviteInfo.
        :type: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")
        self._attrs["createdAt"] = created_at

    @property
    def created_by(self) -> "str":
        """ Gets the created_by of this InviteInfo.
        """
        return self._attrs.get("createdBy")

    @created_by.setter
    def created_by(self, created_by: "str"):
        """Sets the created_by of this InviteInfo.


        :param created_by: The created_by of this InviteInfo.
        :type: str
        """
        if created_by is None:
            raise ValueError("Invalid value for `created_by`, must not be `None`")
        self._attrs["createdBy"] = created_by

    @property
    def email(self) -> "str":
        """ Gets the email of this InviteInfo.
        """
        return self._attrs.get("email")

    @email.setter
    def email(self, email: "str"):
        """Sets the email of this InviteInfo.


        :param email: The email of this InviteInfo.
        :type: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")
        self._attrs["email"] = email

    @property
    def errors(self) -> "List[InviteInfoErrorsItems]":
        """ Gets the errors of this InviteInfo.
        """
        return [InviteInfoErrorsItems._from_dict(i) for i in self._attrs.get("errors")]

    @errors.setter
    def errors(self, errors: "List[InviteInfoErrorsItems]"):
        """Sets the errors of this InviteInfo.


        :param errors: The errors of this InviteInfo.
        :type: List[InviteInfoErrorsItems]
        """
        if errors is None:
            raise ValueError("Invalid value for `errors`, must not be `None`")
        self._attrs["errors"] = errors

    @property
    def expires_at(self) -> "datetime":
        """ Gets the expires_at of this InviteInfo.
        """
        return self._attrs.get("expiresAt")

    @expires_at.setter
    def expires_at(self, expires_at: "datetime"):
        """Sets the expires_at of this InviteInfo.


        :param expires_at: The expires_at of this InviteInfo.
        :type: datetime
        """
        if expires_at is None:
            raise ValueError("Invalid value for `expires_at`, must not be `None`")
        self._attrs["expiresAt"] = expires_at

    @property
    def groups(self) -> "List[str]":
        """ Gets the groups of this InviteInfo.
        """
        return self._attrs.get("groups")

    @groups.setter
    def groups(self, groups: "List[str]"):
        """Sets the groups of this InviteInfo.


        :param groups: The groups of this InviteInfo.
        :type: List[str]
        """
        if groups is None:
            raise ValueError("Invalid value for `groups`, must not be `None`")
        self._attrs["groups"] = groups

    @property
    def invite_id(self) -> "str":
        """ Gets the invite_id of this InviteInfo.
        """
        return self._attrs.get("inviteID")

    @invite_id.setter
    def invite_id(self, invite_id: "str"):
        """Sets the invite_id of this InviteInfo.


        :param invite_id: The invite_id of this InviteInfo.
        :type: str
        """
        if invite_id is None:
            raise ValueError("Invalid value for `invite_id`, must not be `None`")
        self._attrs["inviteID"] = invite_id

    @property
    def status(self) -> "StatusEnum":
        """ Gets the status of this InviteInfo.
        """
        return StatusEnum.from_value(self._attrs.get("status"))

    @status.setter
    def status(self, status: "str"):
        """Sets the status of this InviteInfo.


        :param status: The status of this InviteInfo.
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")
        if isinstance(status, Enum):
            self._attrs["status"] = status.value
        else:
            self._attrs["status"] = status  # If you supply a string, we presume you know the service will take it.

    @property
    def tenant(self) -> "str":
        """ Gets the tenant of this InviteInfo.
        """
        return self._attrs.get("tenant")

    @tenant.setter
    def tenant(self, tenant: "str"):
        """Sets the tenant of this InviteInfo.


        :param tenant: The tenant of this InviteInfo.
        :type: str
        """
        if tenant is None:
            raise ValueError("Invalid value for `tenant`, must not be `None`")
        self._attrs["tenant"] = tenant

    @property
    def updated_at(self) -> "datetime":
        """ Gets the updated_at of this InviteInfo.
        """
        return self._attrs.get("updatedAt")

    @updated_at.setter
    def updated_at(self, updated_at: "datetime"):
        """Sets the updated_at of this InviteInfo.


        :param updated_at: The updated_at of this InviteInfo.
        :type: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")
        self._attrs["updatedAt"] = updated_at

    @property
    def updated_by(self) -> "str":
        """ Gets the updated_by of this InviteInfo.
        """
        return self._attrs.get("updatedBy")

    @updated_by.setter
    def updated_by(self, updated_by: "str"):
        """Sets the updated_by of this InviteInfo.


        :param updated_by: The updated_by of this InviteInfo.
        :type: str
        """
        if updated_by is None:
            raise ValueError("Invalid value for `updated_by`, must not be `None`")
        self._attrs["updatedBy"] = updated_by

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class TenantInfo(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "TenantInfo":
        instance = TenantInfo.__new__(TenantInfo)
        instance._attrs = model
        return instance

    def __init__(self, created_at: "datetime", created_by: "str", name: "str", status: "str", **extra):
        """TenantInfo"""

        self._attrs = dict()
        if created_at is not None:
            self._attrs["createdAt"] = created_at
        if created_by is not None:
            self._attrs["createdBy"] = created_by
        if name is not None:
            self._attrs["name"] = name
        if status is not None:
            self._attrs["status"] = status
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def created_at(self) -> "datetime":
        """ Gets the created_at of this TenantInfo.
        """
        return self._attrs.get("createdAt")

    @created_at.setter
    def created_at(self, created_at: "datetime"):
        """Sets the created_at of this TenantInfo.


        :param created_at: The created_at of this TenantInfo.
        :type: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")
        self._attrs["createdAt"] = created_at

    @property
    def created_by(self) -> "str":
        """ Gets the created_by of this TenantInfo.
        """
        return self._attrs.get("createdBy")

    @created_by.setter
    def created_by(self, created_by: "str"):
        """Sets the created_by of this TenantInfo.


        :param created_by: The created_by of this TenantInfo.
        :type: str
        """
        if created_by is None:
            raise ValueError("Invalid value for `created_by`, must not be `None`")
        self._attrs["createdBy"] = created_by

    @property
    def name(self) -> "str":
        """ Gets the name of this TenantInfo.
        """
        return self._attrs.get("name")

    @name.setter
    def name(self, name: "str"):
        """Sets the name of this TenantInfo.


        :param name: The name of this TenantInfo.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        self._attrs["name"] = name

    @property
    def status(self) -> "str":
        """ Gets the status of this TenantInfo.
        """
        return self._attrs.get("status")

    @status.setter
    def status(self, status: "str"):
        """Sets the status of this TenantInfo.


        :param status: The status of this TenantInfo.
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")
        self._attrs["status"] = status

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class ActionEnum(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    RESEND = "resend"

    @staticmethod
    def from_value(value: str):
        if value == "accept":
            return ActionEnum.ACCEPT
        if value == "reject":
            return ActionEnum.REJECT
        if value == "resend":
            return ActionEnum.RESEND


class UpdateInviteBody(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "UpdateInviteBody":
        instance = UpdateInviteBody.__new__(UpdateInviteBody)
        instance._attrs = model
        return instance

    def __init__(self, action: "str", **extra):
        """UpdateInviteBody"""

        self._attrs = dict()
        if action is not None:
            self._attrs["action"] = action
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def action(self) -> "ActionEnum":
        """ Gets the action of this UpdateInviteBody.
        """
        return ActionEnum.from_value(self._attrs.get("action"))

    @action.setter
    def action(self, action: "str"):
        """Sets the action of this UpdateInviteBody.


        :param action: The action of this UpdateInviteBody.
        :type: str
        """
        if action is None:
            raise ValueError("Invalid value for `action`, must not be `None`")
        if isinstance(action, Enum):
            self._attrs["action"] = action.value
        else:
            self._attrs["action"] = action  # If you supply a string, we presume you know the service will take it.

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}
