# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import json


class PostIngestResponse(object):
    def __init__(self,
                 code,
                 message):
        self._code = code,
        self._message = message

    @property
    def code(self):
        """Return the code attribute of the Ingest Response"""
        return self._code

    @property
    def message(self):
        """Return the message attribute of the Ingest Response"""
        return self._message


class EventData(object):

    def __init__(self, body, host, source, sourcetype,
                 attributes, nanos=None, timestamp=None):
        self.body = body
        self.host = host
        self.source = source
        self.sourcetype = sourcetype
        self.attributes = attributes
        self.nanos = nanos
        self.timestamp = timestamp

    def reprJSON(self):
        return dict(body=self.body, host=self.host,
                    source=self.source, sourcetype=self.sourcetype,
                    attributes=self.attributes,
                    timestamp=self.timestamp, nanos=self.nanos)


class Attributes(object):

    def __init__(self, data):
        self.data = data

    def reprJSON(self):
        return dict(attributes=self.data)


class Metric(object):

    def __init__(self, name, value, dimensions, unit):
        self.name = name
        self.value = value
        self.dimensions = dimensions
        self.unit = unit

    def reprJSON(self):
        return dict(Name=self.name, Value=self.value,
                    Dimensions=self.dimensions, Unit=self.unit)


class MetricEvent(object):

    def __init__(self, body, host, source, sourcetype,
                 timestamp, nanos, metricattributes, id):
        self.body = body
        self.host = host
        self.source = source
        self.sourcetype = sourcetype
        self.metricattributes = metricattributes
        self.nanos = nanos
        self.timestamp = timestamp
        self.id = id

    def reprJSON(self):
        return dict(Body=self.body, Host=self.host,
                    Source=self.source, Sourcetype=self.sourcetype,
                    Attributes=self.metricattributes, Timestamp=self.timestamp,
                    Nanos=self.nanos, ID=self.id)


class MetricAttribute(object):

    def __init__(self, defaulttype, defaultdimensions, defaultunit):
        self.defaulttype = defaulttype
        self.defaultdimensions = defaultdimensions
        self.defaultunit = defaultunit

    def reprJSON(self):
        return dict(DefaultType=self.defaulttype,
                    DefaultDimensions=self.defaultdimensions,
                    DefaultUnit=self.defaultunit)


class IngestEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, EventData):
            return obj.reprJSON()
        elif isinstance(obj, Attributes):
            return obj.reprJSON()
        elif isinstance(obj, MetricAttribute):
            return obj.reprJSON()
        elif isinstance(obj, MetricEvent):
            return obj.reprJSON()
        elif isinstance(obj, Metric):
            return obj.reprJSON()
        else:
            type_name = obj.__class__.__name__
            raise TypeError(f"Object of type '{type_name}' "
                            f"is not JSON serializable")
