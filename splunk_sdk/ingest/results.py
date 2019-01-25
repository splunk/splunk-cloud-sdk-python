class Event(object):

    def __init__(self,
                 body,
                 host=None,
                 attributes=None,
                 nanos=None,
                 source=None,
                 sourceType=None,
                 id=None):
        self._attributes = attributes,
        self._body = body,
        self._nanos = nanos,
        self._source = source,
        self._sourceType = sourceType,
        self._host = host,
        self._id = id


    @property
    def event(self):
        """Return the attributes of the Ingest Event"""
        return self._attributes

    @event.setter
    def status(self, attributes):
        """Set the Attribute of the Ingest API"""
        self._attributes = attributes

    @property
    def event(self):
        """Return the Body of the Ingest Event"""
        return self._body

    @event.setter
    def status(self, body):
        """Set the Body of the Ingest API"""
        self._body = body

    @property
    def event(self):
        """Return the Nanos of the Ingest Event"""
        return self._nanos

    @event.setter
    def status(self, nanos):
        """Set the Nanos of the Ingest API"""
        self._nanos = nanos

    @property
    def event(self):
        """Return the Source of the Ingest Event"""
        return self._source

    @event.setter
    def status(self, source):
        """Set the Source of the Ingest Event"""
        self._source = source

    @property
    def event(self):
        """Return the SourceType of the Ingest Event"""
        return self._sourceType

    @event.setter
    def status(self, sourceType):
        """Set the SourceType of the Ingest Event"""
        self._sourceType = sourceType

    @property
    def event(self):
        """Return the Host of the Ingest Event"""
        return self._host

    @event.setter
    def status(self, host):
        """Set the Host of the Ingest Event"""
        self._host = host

    @property
    def event(self):
        """Return the ID of the Ingest Event"""
        return self._id

    @event.setter
    def status(self, id):
        """Set the Source of the Ingest Event"""
        self._id = id



