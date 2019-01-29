

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
