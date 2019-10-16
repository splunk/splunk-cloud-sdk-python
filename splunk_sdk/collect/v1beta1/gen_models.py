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
    SDC Service: Collect Service

    With the Collect service in Splunk Cloud Services, you can manage how data collection jobs ingest event and metric data.

    OpenAPI spec version: v1beta1.7 (recommended default)
    Generated by: https://openapi-generator.tech
"""


from datetime import datetime
from typing import List, Dict
from splunk_sdk.common.sscmodel import SSCModel
from splunk_sdk.base_client import dictify, inflate
from enum import Enum



class BaseJob(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "BaseJob":
        instance = BaseJob.__new__(BaseJob)
        instance._attrs = model
        return instance

    def __init__(self, connector_id: "str", name: "str", schedule: "str", create_user_id: "str" = None, created_at: "datetime" = None, id: "str" = None, last_modified_at: "datetime" = None, last_update_user_id: "str" = None, scheduled: "bool" = True, tenant: "str" = None, **extra):
        """BaseJob"""

        self._attrs = dict()
        if connector_id is not None:
            self._attrs["connectorID"] = connector_id
        if name is not None:
            self._attrs["name"] = name
        if schedule is not None:
            self._attrs["schedule"] = schedule
        if create_user_id is not None:
            self._attrs["createUserID"] = create_user_id
        if created_at is not None:
            self._attrs["createdAt"] = created_at
        if id is not None:
            self._attrs["id"] = id
        if last_modified_at is not None:
            self._attrs["lastModifiedAt"] = last_modified_at
        if last_update_user_id is not None:
            self._attrs["lastUpdateUserID"] = last_update_user_id
        if scheduled is not None:
            self._attrs["scheduled"] = scheduled
        if tenant is not None:
            self._attrs["tenant"] = tenant
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def connector_id(self) -> "str":
        """ Gets the connector_id of this BaseJob.
        The ID of the connector used in the job.
        """
        return self._attrs.get("connectorID")

    @connector_id.setter
    def connector_id(self, connector_id: "str"):
        """Sets the connector_id of this BaseJob.

        The ID of the connector used in the job.

        :param connector_id: The connector_id of this BaseJob.
        :type: str
        """
        if connector_id is None:
            raise ValueError("Invalid value for `connector_id`, must not be `None`")
        self._attrs["connectorID"] = connector_id

    @property
    def name(self) -> "str":
        """ Gets the name of this BaseJob.
        """
        return self._attrs.get("name")

    @name.setter
    def name(self, name: "str"):
        """Sets the name of this BaseJob.


        :param name: The name of this BaseJob.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        self._attrs["name"] = name

    @property
    def schedule(self) -> "str":
        """ Gets the schedule of this BaseJob.
        The cron schedule, in UTC time format.
        """
        return self._attrs.get("schedule")

    @schedule.setter
    def schedule(self, schedule: "str"):
        """Sets the schedule of this BaseJob.

        The cron schedule, in UTC time format.

        :param schedule: The schedule of this BaseJob.
        :type: str
        """
        if schedule is None:
            raise ValueError("Invalid value for `schedule`, must not be `None`")
        self._attrs["schedule"] = schedule

    @property
    def create_user_id(self) -> "str":
        """ Gets the create_user_id of this BaseJob.
        """
        return self._attrs.get("createUserID")

    @create_user_id.setter
    def create_user_id(self, create_user_id: "str"):
        """Sets the create_user_id of this BaseJob.


        :param create_user_id: The create_user_id of this BaseJob.
        :type: str
        """
        self._attrs["createUserID"] = create_user_id

    @property
    def created_at(self) -> "datetime":
        """ Gets the created_at of this BaseJob.
        """
        return self._attrs.get("createdAt")

    @created_at.setter
    def created_at(self, created_at: "datetime"):
        """Sets the created_at of this BaseJob.


        :param created_at: The created_at of this BaseJob.
        :type: datetime
        """
        self._attrs["createdAt"] = created_at

    @property
    def id(self) -> "str":
        """ Gets the id of this BaseJob.
        """
        return self._attrs.get("id")

    @id.setter
    def id(self, id: "str"):
        """Sets the id of this BaseJob.


        :param id: The id of this BaseJob.
        :type: str
        """
        self._attrs["id"] = id

    @property
    def last_modified_at(self) -> "datetime":
        """ Gets the last_modified_at of this BaseJob.
        """
        return self._attrs.get("lastModifiedAt")

    @last_modified_at.setter
    def last_modified_at(self, last_modified_at: "datetime"):
        """Sets the last_modified_at of this BaseJob.


        :param last_modified_at: The last_modified_at of this BaseJob.
        :type: datetime
        """
        self._attrs["lastModifiedAt"] = last_modified_at

    @property
    def last_update_user_id(self) -> "str":
        """ Gets the last_update_user_id of this BaseJob.
        """
        return self._attrs.get("lastUpdateUserID")

    @last_update_user_id.setter
    def last_update_user_id(self, last_update_user_id: "str"):
        """Sets the last_update_user_id of this BaseJob.


        :param last_update_user_id: The last_update_user_id of this BaseJob.
        :type: str
        """
        self._attrs["lastUpdateUserID"] = last_update_user_id

    @property
    def scheduled(self) -> "bool":
        """ Gets the scheduled of this BaseJob.
        Defines whether a job is scheduled or not
        """
        return self._attrs.get("scheduled")

    @scheduled.setter
    def scheduled(self, scheduled: "bool"):
        """Sets the scheduled of this BaseJob.

        Defines whether a job is scheduled or not

        :param scheduled: The scheduled of this BaseJob.
        :type: bool
        """
        self._attrs["scheduled"] = scheduled

    @property
    def tenant(self) -> "str":
        """ Gets the tenant of this BaseJob.
        """
        return self._attrs.get("tenant")

    @tenant.setter
    def tenant(self, tenant: "str"):
        """Sets the tenant of this BaseJob.


        :param tenant: The tenant of this BaseJob.
        :type: str
        """
        self._attrs["tenant"] = tenant

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class ScalePolicy(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "ScalePolicy":
        instance = ScalePolicy.__new__(ScalePolicy)
        instance._attrs = model
        return instance

    def __init__(self, static: "StaticScale", **extra):
        """ScalePolicy"""

        self._attrs = dict()
        if static is not None:
            self._attrs["static"] = static.to_dict()
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def static(self) -> "StaticScale":
        """ Gets the static of this ScalePolicy.
        """
        return StaticScale._from_dict(self._attrs["static"])

    @static.setter
    def static(self, static: "StaticScale"):
        """Sets the static of this ScalePolicy.


        :param static: The static of this ScalePolicy.
        :type: StaticScale
        """
        if static is None:
            raise ValueError("Invalid value for `static`, must not be `None`")
        self._attrs["static"] = static.to_dict()

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class StaticScale(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "StaticScale":
        instance = StaticScale.__new__(StaticScale)
        instance._attrs = model
        return instance

    def __init__(self, workers: "int", **extra):
        """StaticScale"""

        self._attrs = dict()
        if workers is not None:
            self._attrs["workers"] = workers
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def workers(self) -> "int":
        """ Gets the workers of this StaticScale.
        The number of collect workers.
        """
        return self._attrs.get("workers")

    @workers.setter
    def workers(self, workers: "int"):
        """Sets the workers of this StaticScale.

        The number of collect workers.

        :param workers: The workers of this StaticScale.
        :type: int
        """
        if workers is None:
            raise ValueError("Invalid value for `workers`, must not be `None`")
        self._attrs["workers"] = workers

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class DeleteJobsResponse(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "DeleteJobsResponse":
        instance = DeleteJobsResponse.__new__(DeleteJobsResponse)
        instance._attrs = model
        return instance

    def __init__(self, count: "int", **extra):
        """DeleteJobsResponse"""

        self._attrs = dict()
        if count is not None:
            self._attrs["count"] = count
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def count(self) -> "int":
        """ Gets the count of this DeleteJobsResponse.
        """
        return self._attrs.get("count")

    @count.setter
    def count(self, count: "int"):
        """Sets the count of this DeleteJobsResponse.


        :param count: The count of this DeleteJobsResponse.
        :type: int
        """
        if count is None:
            raise ValueError("Invalid value for `count`, must not be `None`")
        self._attrs["count"] = count

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class Error(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "Error":
        instance = Error.__new__(Error)
        instance._attrs = model
        return instance

    def __init__(self, code: "str", message: "str", details: "object" = None, more_info: "str" = None, **extra):
        """Error"""

        self._attrs = dict()
        if code is not None:
            self._attrs["code"] = code
        if message is not None:
            self._attrs["message"] = message
        if details is not None:
            self._attrs["details"] = details
        if more_info is not None:
            self._attrs["moreInfo"] = more_info
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def code(self) -> "str":
        """ Gets the code of this Error.
        """
        return self._attrs.get("code")

    @code.setter
    def code(self, code: "str"):
        """Sets the code of this Error.


        :param code: The code of this Error.
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")
        self._attrs["code"] = code

    @property
    def message(self) -> "str":
        """ Gets the message of this Error.
        """
        return self._attrs.get("message")

    @message.setter
    def message(self, message: "str"):
        """Sets the message of this Error.


        :param message: The message of this Error.
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")
        self._attrs["message"] = message

    @property
    def details(self) -> "dict":
        """ Gets the details of this Error.
        The optional details of the error.
        """
        return self._attrs.get("details")

    @details.setter
    def details(self, details: "dict"):
        """Sets the details of this Error.

        The optional details of the error.

        :param details: The details of this Error.
        :type: object
        """
        self._attrs["details"] = details

    @property
    def more_info(self) -> "str":
        """ Gets the more_info of this Error.
        An optional link to a web page with more information on the error.
        """
        return self._attrs.get("moreInfo")

    @more_info.setter
    def more_info(self, more_info: "str"):
        """Sets the more_info of this Error.

        An optional link to a web page with more information on the error.

        :param more_info: The more_info of this Error.
        :type: str
        """
        self._attrs["moreInfo"] = more_info

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class EventExtraField(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "EventExtraField":
        instance = EventExtraField.__new__(EventExtraField)
        instance._attrs = model
        return instance

    def __init__(self, name: "str", value: "str", **extra):
        """EventExtraField"""

        self._attrs = dict()
        if name is not None:
            self._attrs["name"] = name
        if value is not None:
            self._attrs["value"] = value
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def name(self) -> "str":
        """ Gets the name of this EventExtraField.
        Field name
        """
        return self._attrs.get("name")

    @name.setter
    def name(self, name: "str"):
        """Sets the name of this EventExtraField.

        Field name

        :param name: The name of this EventExtraField.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        self._attrs["name"] = name

    @property
    def value(self) -> "str":
        """ Gets the value of this EventExtraField.
        Field value
        """
        return self._attrs.get("value")

    @value.setter
    def value(self, value: "str"):
        """Sets the value of this EventExtraField.

        Field value

        :param value: The value of this EventExtraField.
        :type: str
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")
        self._attrs["value"] = value

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class Job(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "Job":
        instance = Job.__new__(Job)
        instance._attrs = model
        return instance

    def __init__(self, connector_id: "str", name: "str", parameters: "object", scale_policy: "ScalePolicy", schedule: "str", create_user_id: "str" = None, created_at: "datetime" = None, event_extra_fields: "List[EventExtraField]" = None, id: "str" = None, last_modified_at: "datetime" = None, last_update_user_id: "str" = None, scheduled: "bool" = True, tenant: "str" = None, **extra):
        """Job"""

        self._attrs = dict()
        if connector_id is not None:
            self._attrs["connectorID"] = connector_id
        if name is not None:
            self._attrs["name"] = name
        if parameters is not None:
            self._attrs["parameters"] = parameters
        if scale_policy is not None:
            self._attrs["scalePolicy"] = scale_policy.to_dict()
        if schedule is not None:
            self._attrs["schedule"] = schedule
        if create_user_id is not None:
            self._attrs["createUserID"] = create_user_id
        if created_at is not None:
            self._attrs["createdAt"] = created_at
        if event_extra_fields is not None:
            self._attrs["eventExtraFields"] = event_extra_fields
        if id is not None:
            self._attrs["id"] = id
        if last_modified_at is not None:
            self._attrs["lastModifiedAt"] = last_modified_at
        if last_update_user_id is not None:
            self._attrs["lastUpdateUserID"] = last_update_user_id
        if scheduled is not None:
            self._attrs["scheduled"] = scheduled
        if tenant is not None:
            self._attrs["tenant"] = tenant
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def connector_id(self) -> "str":
        """ Gets the connector_id of this Job.
        The ID of the connector used in the job.
        """
        return self._attrs.get("connectorID")

    @connector_id.setter
    def connector_id(self, connector_id: "str"):
        """Sets the connector_id of this Job.

        The ID of the connector used in the job.

        :param connector_id: The connector_id of this Job.
        :type: str
        """
        if connector_id is None:
            raise ValueError("Invalid value for `connector_id`, must not be `None`")
        self._attrs["connectorID"] = connector_id

    @property
    def name(self) -> "str":
        """ Gets the name of this Job.
        """
        return self._attrs.get("name")

    @name.setter
    def name(self, name: "str"):
        """Sets the name of this Job.


        :param name: The name of this Job.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        self._attrs["name"] = name

    @property
    def parameters(self) -> "dict":
        """ Gets the parameters of this Job.
        The configuration of the connector used in the job.
        """
        return self._attrs.get("parameters")

    @parameters.setter
    def parameters(self, parameters: "dict"):
        """Sets the parameters of this Job.

        The configuration of the connector used in the job.

        :param parameters: The parameters of this Job.
        :type: object
        """
        if parameters is None:
            raise ValueError("Invalid value for `parameters`, must not be `None`")
        self._attrs["parameters"] = parameters

    @property
    def scale_policy(self) -> "ScalePolicy":
        """ Gets the scale_policy of this Job.
        """
        return ScalePolicy._from_dict(self._attrs["scalePolicy"])

    @scale_policy.setter
    def scale_policy(self, scale_policy: "ScalePolicy"):
        """Sets the scale_policy of this Job.


        :param scale_policy: The scale_policy of this Job.
        :type: ScalePolicy
        """
        if scale_policy is None:
            raise ValueError("Invalid value for `scale_policy`, must not be `None`")
        self._attrs["scalePolicy"] = scale_policy.to_dict()

    @property
    def schedule(self) -> "str":
        """ Gets the schedule of this Job.
        The cron schedule, in UTC time format.
        """
        return self._attrs.get("schedule")

    @schedule.setter
    def schedule(self, schedule: "str"):
        """Sets the schedule of this Job.

        The cron schedule, in UTC time format.

        :param schedule: The schedule of this Job.
        :type: str
        """
        if schedule is None:
            raise ValueError("Invalid value for `schedule`, must not be `None`")
        self._attrs["schedule"] = schedule

    @property
    def create_user_id(self) -> "str":
        """ Gets the create_user_id of this Job.
        """
        return self._attrs.get("createUserID")

    @create_user_id.setter
    def create_user_id(self, create_user_id: "str"):
        """Sets the create_user_id of this Job.


        :param create_user_id: The create_user_id of this Job.
        :type: str
        """
        self._attrs["createUserID"] = create_user_id

    @property
    def created_at(self) -> "datetime":
        """ Gets the created_at of this Job.
        """
        return self._attrs.get("createdAt")

    @created_at.setter
    def created_at(self, created_at: "datetime"):
        """Sets the created_at of this Job.


        :param created_at: The created_at of this Job.
        :type: datetime
        """
        self._attrs["createdAt"] = created_at

    @property
    def event_extra_fields(self) -> "List[EventExtraField]":
        """ Gets the event_extra_fields of this Job.
        """
        return [EventExtraField._from_dict(i) for i in self._attrs.get("eventExtraFields")]

    @event_extra_fields.setter
    def event_extra_fields(self, event_extra_fields: "List[EventExtraField]"):
        """Sets the event_extra_fields of this Job.


        :param event_extra_fields: The event_extra_fields of this Job.
        :type: List[EventExtraField]
        """
        self._attrs["eventExtraFields"] = event_extra_fields

    @property
    def id(self) -> "str":
        """ Gets the id of this Job.
        """
        return self._attrs.get("id")

    @id.setter
    def id(self, id: "str"):
        """Sets the id of this Job.


        :param id: The id of this Job.
        :type: str
        """
        self._attrs["id"] = id

    @property
    def last_modified_at(self) -> "datetime":
        """ Gets the last_modified_at of this Job.
        """
        return self._attrs.get("lastModifiedAt")

    @last_modified_at.setter
    def last_modified_at(self, last_modified_at: "datetime"):
        """Sets the last_modified_at of this Job.


        :param last_modified_at: The last_modified_at of this Job.
        :type: datetime
        """
        self._attrs["lastModifiedAt"] = last_modified_at

    @property
    def last_update_user_id(self) -> "str":
        """ Gets the last_update_user_id of this Job.
        """
        return self._attrs.get("lastUpdateUserID")

    @last_update_user_id.setter
    def last_update_user_id(self, last_update_user_id: "str"):
        """Sets the last_update_user_id of this Job.


        :param last_update_user_id: The last_update_user_id of this Job.
        :type: str
        """
        self._attrs["lastUpdateUserID"] = last_update_user_id

    @property
    def scheduled(self) -> "bool":
        """ Gets the scheduled of this Job.
        Defines whether a job is scheduled or not
        """
        return self._attrs.get("scheduled")

    @scheduled.setter
    def scheduled(self, scheduled: "bool"):
        """Sets the scheduled of this Job.

        Defines whether a job is scheduled or not

        :param scheduled: The scheduled of this Job.
        :type: bool
        """
        self._attrs["scheduled"] = scheduled

    @property
    def tenant(self) -> "str":
        """ Gets the tenant of this Job.
        """
        return self._attrs.get("tenant")

    @tenant.setter
    def tenant(self, tenant: "str"):
        """Sets the tenant of this Job.


        :param tenant: The tenant of this Job.
        :type: str
        """
        self._attrs["tenant"] = tenant

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class JobPatch(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "JobPatch":
        instance = JobPatch.__new__(JobPatch)
        instance._attrs = model
        return instance

    def __init__(self, connector_id: "str" = None, event_extra_fields: "List[EventExtraField]" = None, name: "str" = None, parameters: "object" = None, scale_policy: "ScalePolicy" = None, schedule: "str" = None, scheduled: "bool" = None, **extra):
        """JobPatch"""

        self._attrs = dict()
        if connector_id is not None:
            self._attrs["connectorID"] = connector_id
        if event_extra_fields is not None:
            self._attrs["eventExtraFields"] = event_extra_fields
        if name is not None:
            self._attrs["name"] = name
        if parameters is not None:
            self._attrs["parameters"] = parameters
        if scale_policy is not None:
            self._attrs["scalePolicy"] = scale_policy.to_dict()
        if schedule is not None:
            self._attrs["schedule"] = schedule
        if scheduled is not None:
            self._attrs["scheduled"] = scheduled
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def connector_id(self) -> "str":
        """ Gets the connector_id of this JobPatch.
        The ID of the connector used in the job.
        """
        return self._attrs.get("connectorID")

    @connector_id.setter
    def connector_id(self, connector_id: "str"):
        """Sets the connector_id of this JobPatch.

        The ID of the connector used in the job.

        :param connector_id: The connector_id of this JobPatch.
        :type: str
        """
        self._attrs["connectorID"] = connector_id

    @property
    def event_extra_fields(self) -> "List[EventExtraField]":
        """ Gets the event_extra_fields of this JobPatch.
        """
        return [EventExtraField._from_dict(i) for i in self._attrs.get("eventExtraFields")]

    @event_extra_fields.setter
    def event_extra_fields(self, event_extra_fields: "List[EventExtraField]"):
        """Sets the event_extra_fields of this JobPatch.


        :param event_extra_fields: The event_extra_fields of this JobPatch.
        :type: List[EventExtraField]
        """
        self._attrs["eventExtraFields"] = event_extra_fields

    @property
    def name(self) -> "str":
        """ Gets the name of this JobPatch.
        The job name
        """
        return self._attrs.get("name")

    @name.setter
    def name(self, name: "str"):
        """Sets the name of this JobPatch.

        The job name

        :param name: The name of this JobPatch.
        :type: str
        """
        self._attrs["name"] = name

    @property
    def parameters(self) -> "dict":
        """ Gets the parameters of this JobPatch.
        The configuration of the connector used in the job.
        """
        return self._attrs.get("parameters")

    @parameters.setter
    def parameters(self, parameters: "dict"):
        """Sets the parameters of this JobPatch.

        The configuration of the connector used in the job.

        :param parameters: The parameters of this JobPatch.
        :type: object
        """
        self._attrs["parameters"] = parameters

    @property
    def scale_policy(self) -> "ScalePolicy":
        """ Gets the scale_policy of this JobPatch.
        """
        return ScalePolicy._from_dict(self._attrs["scalePolicy"])

    @scale_policy.setter
    def scale_policy(self, scale_policy: "ScalePolicy"):
        """Sets the scale_policy of this JobPatch.


        :param scale_policy: The scale_policy of this JobPatch.
        :type: ScalePolicy
        """
        self._attrs["scalePolicy"] = scale_policy.to_dict()

    @property
    def schedule(self) -> "str":
        """ Gets the schedule of this JobPatch.
        The cron schedule, in UTC time format.
        """
        return self._attrs.get("schedule")

    @schedule.setter
    def schedule(self, schedule: "str"):
        """Sets the schedule of this JobPatch.

        The cron schedule, in UTC time format.

        :param schedule: The schedule of this JobPatch.
        :type: str
        """
        self._attrs["schedule"] = schedule

    @property
    def scheduled(self) -> "bool":
        """ Gets the scheduled of this JobPatch.
        Defines wheather a job is scheduled or not
        """
        return self._attrs.get("scheduled")

    @scheduled.setter
    def scheduled(self, scheduled: "bool"):
        """Sets the scheduled of this JobPatch.

        Defines wheather a job is scheduled or not

        :param scheduled: The scheduled of this JobPatch.
        :type: bool
        """
        self._attrs["scheduled"] = scheduled

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class JobsPatch(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "JobsPatch":
        instance = JobsPatch.__new__(JobsPatch)
        instance._attrs = model
        return instance

    def __init__(self, connector_id: "str" = None, event_extra_fields: "List[EventExtraField]" = None, scale_policy: "ScalePolicy" = None, **extra):
        """JobsPatch"""

        self._attrs = dict()
        if connector_id is not None:
            self._attrs["connectorID"] = connector_id
        if event_extra_fields is not None:
            self._attrs["eventExtraFields"] = event_extra_fields
        if scale_policy is not None:
            self._attrs["scalePolicy"] = scale_policy.to_dict()
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def connector_id(self) -> "str":
        """ Gets the connector_id of this JobsPatch.
        The ID of the connector used in the job.
        """
        return self._attrs.get("connectorID")

    @connector_id.setter
    def connector_id(self, connector_id: "str"):
        """Sets the connector_id of this JobsPatch.

        The ID of the connector used in the job.

        :param connector_id: The connector_id of this JobsPatch.
        :type: str
        """
        self._attrs["connectorID"] = connector_id

    @property
    def event_extra_fields(self) -> "List[EventExtraField]":
        """ Gets the event_extra_fields of this JobsPatch.
        """
        return [EventExtraField._from_dict(i) for i in self._attrs.get("eventExtraFields")]

    @event_extra_fields.setter
    def event_extra_fields(self, event_extra_fields: "List[EventExtraField]"):
        """Sets the event_extra_fields of this JobsPatch.


        :param event_extra_fields: The event_extra_fields of this JobsPatch.
        :type: List[EventExtraField]
        """
        self._attrs["eventExtraFields"] = event_extra_fields

    @property
    def scale_policy(self) -> "ScalePolicy":
        """ Gets the scale_policy of this JobsPatch.
        """
        return ScalePolicy._from_dict(self._attrs["scalePolicy"])

    @scale_policy.setter
    def scale_policy(self, scale_policy: "ScalePolicy"):
        """Sets the scale_policy of this JobsPatch.


        :param scale_policy: The scale_policy of this JobsPatch.
        :type: ScalePolicy
        """
        self._attrs["scalePolicy"] = scale_policy.to_dict()

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class ListJobsResponse(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "ListJobsResponse":
        instance = ListJobsResponse.__new__(ListJobsResponse)
        instance._attrs = model
        return instance

    def __init__(self, data: "List[BaseJob]" = None, **extra):
        """ListJobsResponse"""

        self._attrs = dict()
        if data is not None:
            self._attrs["data"] = data
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def data(self) -> "List[BaseJob]":
        """ Gets the data of this ListJobsResponse.
        """
        return [BaseJob._from_dict(i) for i in self._attrs.get("data")]

    @data.setter
    def data(self, data: "List[BaseJob]"):
        """Sets the data of this ListJobsResponse.


        :param data: The data of this ListJobsResponse.
        :type: List[BaseJob]
        """
        self._attrs["data"] = data

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class Metadata(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "Metadata":
        instance = Metadata.__new__(Metadata)
        instance._attrs = model
        return instance

    def __init__(self, failures: "int", total_match_jobs: "int", **extra):
        """Metadata"""

        self._attrs = dict()
        if failures is not None:
            self._attrs["failures"] = failures
        if total_match_jobs is not None:
            self._attrs["totalMatchJobs"] = total_match_jobs
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def failures(self) -> "int":
        """ Gets the failures of this Metadata.
        The number of jobs that failed to update.
        """
        return self._attrs.get("failures")

    @failures.setter
    def failures(self, failures: "int"):
        """Sets the failures of this Metadata.

        The number of jobs that failed to update.

        :param failures: The failures of this Metadata.
        :type: int
        """
        if failures is None:
            raise ValueError("Invalid value for `failures`, must not be `None`")
        self._attrs["failures"] = failures

    @property
    def total_match_jobs(self) -> "int":
        """ Gets the total_match_jobs of this Metadata.
        The number of jobs which match the query criteria.
        """
        return self._attrs.get("totalMatchJobs")

    @total_match_jobs.setter
    def total_match_jobs(self, total_match_jobs: "int"):
        """Sets the total_match_jobs of this Metadata.

        The number of jobs which match the query criteria.

        :param total_match_jobs: The total_match_jobs of this Metadata.
        :type: int
        """
        if total_match_jobs is None:
            raise ValueError("Invalid value for `total_match_jobs`, must not be `None`")
        self._attrs["totalMatchJobs"] = total_match_jobs

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class PatchJobResult(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "PatchJobResult":
        instance = PatchJobResult.__new__(PatchJobResult)
        instance._attrs = model
        return instance

    def __init__(self, id: "str", updated: "bool", error: "Error" = None, **extra):
        """PatchJobResult"""

        self._attrs = dict()
        if id is not None:
            self._attrs["id"] = id
        if updated is not None:
            self._attrs["updated"] = updated
        if error is not None:
            self._attrs["error"] = error.to_dict()
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def id(self) -> "str":
        """ Gets the id of this PatchJobResult.
        The Job ID.
        """
        return self._attrs.get("id")

    @id.setter
    def id(self, id: "str"):
        """Sets the id of this PatchJobResult.

        The Job ID.

        :param id: The id of this PatchJobResult.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")
        self._attrs["id"] = id

    @property
    def updated(self) -> "bool":
        """ Gets the updated of this PatchJobResult.
        Successfully updated or not.
        """
        return self._attrs.get("updated")

    @updated.setter
    def updated(self, updated: "bool"):
        """Sets the updated of this PatchJobResult.

        Successfully updated or not.

        :param updated: The updated of this PatchJobResult.
        :type: bool
        """
        if updated is None:
            raise ValueError("Invalid value for `updated`, must not be `None`")
        self._attrs["updated"] = updated

    @property
    def error(self) -> "Error":
        """ Gets the error of this PatchJobResult.
        """
        return Error._from_dict(self._attrs["error"])

    @error.setter
    def error(self, error: "Error"):
        """Sets the error of this PatchJobResult.


        :param error: The error of this PatchJobResult.
        :type: Error
        """
        self._attrs["error"] = error.to_dict()

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class PatchJobsResponse(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "PatchJobsResponse":
        instance = PatchJobsResponse.__new__(PatchJobsResponse)
        instance._attrs = model
        return instance

    def __init__(self, data: "List[PatchJobResult]", metadata: "Metadata", **extra):
        """PatchJobsResponse"""

        self._attrs = dict()
        if data is not None:
            self._attrs["data"] = data
        if metadata is not None:
            self._attrs["metadata"] = metadata.to_dict()
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def data(self) -> "List[PatchJobResult]":
        """ Gets the data of this PatchJobsResponse.
        """
        return [PatchJobResult._from_dict(i) for i in self._attrs.get("data")]

    @data.setter
    def data(self, data: "List[PatchJobResult]"):
        """Sets the data of this PatchJobsResponse.


        :param data: The data of this PatchJobsResponse.
        :type: List[PatchJobResult]
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")
        self._attrs["data"] = data

    @property
    def metadata(self) -> "Metadata":
        """ Gets the metadata of this PatchJobsResponse.
        """
        return Metadata._from_dict(self._attrs["metadata"])

    @metadata.setter
    def metadata(self, metadata: "Metadata"):
        """Sets the metadata of this PatchJobsResponse.


        :param metadata: The metadata of this PatchJobsResponse.
        :type: Metadata
        """
        if metadata is None:
            raise ValueError("Invalid value for `metadata`, must not be `None`")
        self._attrs["metadata"] = metadata.to_dict()

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}


class SingleJobResponse(SSCModel):

    @staticmethod
    def _from_dict(model: dict) -> "SingleJobResponse":
        instance = SingleJobResponse.__new__(SingleJobResponse)
        instance._attrs = model
        return instance

    def __init__(self, data: "Job", **extra):
        """SingleJobResponse"""

        self._attrs = dict()
        if data is not None:
            self._attrs["data"] = data.to_dict()
        for k, v in extra.items():
            self._attrs[k] = v

    @property
    def data(self) -> "Job":
        """ Gets the data of this SingleJobResponse.
        """
        return Job._from_dict(self._attrs["data"])

    @data.setter
    def data(self, data: "Job"):
        """Sets the data of this SingleJobResponse.


        :param data: The data of this SingleJobResponse.
        :type: Job
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")
        self._attrs["data"] = data.to_dict()

    def to_dict(self):
        return {k: v for (k, v) in self._attrs.items() if v is not None}
