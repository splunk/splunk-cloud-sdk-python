from enum import Enum


# TODO: how do we use this model?
class JobStatus(Enum):
    QUEUED = "queued"
    PARSING = "parsing"
    RUNNING = "running"
    FINALIZING = "finalizing"
    FAILED = "failed"
    DONE = "done"


class Job(object):

    def __init__(self,
                 query,
                 extractAllFields,
                 timeFormat=None,
                 module=None,
                 maxTime=None,
                 timeOfSearch=None,
                 queryParameters=None,
                 sid=None,
                 status=None,
                 percentComplete=None,
                 resultsAvailable=None,
                 messages=None):
        self._query = query
        self._extractAllFields = extractAllFields
        self._timeFormat = timeFormat
        self._module = module
        self._maxTime = maxTime
        self._timeOfSearch = timeOfSearch
        self._queryParameters = queryParameters
        self._sid = sid
        self._status = status
        self._percentComplete = percentComplete
        self._resultsAvailable = resultsAvailable
        self._messages = messages

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    @property
    def extractAllFields(self):
        return self._extractAllFields

    @extractAllFields.setter
    def extractAllFields(self, extractAllFields):
        self._extractAllFields = extractAllFields

    @property
    def timeFormat(self):
        return self._timeFormat

    @timeFormat.setter
    def timeFormat(self, timeFormat):
        self._timeFormat = timeFormat

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, module):
        self._module = module

    @property
    def maxTime(self):
        return self._maxTime

    @maxTime.setter
    def maxTime(self, maxTime):
        self._maxTime = maxTime

    @property
    def timeOfSearch(self):
        return self._timeOfSearch

    @timeOfSearch.setter
    def timeOfSearch(self, timeOfSearch):
        self._timeOfSearch = timeOfSearch

    @property
    def queryParameters(self):
        return self._queryParameters

    @queryParameters.setter
    def queryParameters(self, queryParameters):
        self._queryParameters = queryParameters

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        self._sid = sid

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def percentComplete(self):
        return self._percentComplete

    @percentComplete.setter
    def percentComplete(self, percentComplete):
        self._percentComplete = percentComplete

    @property
    def resultsAvailable(self):
        return self._resultsAvailable

    @resultsAvailable.setter
    def resultsAvailable(self, resultsAvailable):
        self._resultsAvailable = resultsAvailable

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, messages):
        self._messages = messages


class UpdateJobResponse(object):

    def __init__(self,
                 messages=None):
        self._messages = messages

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, messages):
        self._messages = messages


class SearchResults(object):
    def __init__(self,
                 messages=None,
                 results=None,
                 fields=None):
        self._messages = messages
        self._results = results
        self._fields = fields

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, messages):
        self._messages = messages

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results = results

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields):
        self._fields = fields


class ResultsNotReadyResponse(object):
    def __init__(self,
                 nextLink=None,
                 wait=None):
        self._nextLink = nextLink
        self._wait = wait

    @property
    def nextLink(self):
        return self._nextLink

    @nextLink.setter
    def nextLink(self, nextLink):
        self._nextLink = nextLink

    @property
    def wait(self):
        return self._wait

    @wait.setter
    def wait(self, wait):
        self._wait = wait


class DispatchState(Enum):
    DONE = 'done'
    FAILED = 'failed'


class MessageTypes(Enum):
    INFO = 'INFO'
    DEBUG = 'INFO'
    FATAL = 'FATAL'
    ERROR = 'ERROR'


class SearchJobMessage(object):
    def __init__(self,
                 text=None,
                 type=None):
        self._text = text
        self._type = type

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type
