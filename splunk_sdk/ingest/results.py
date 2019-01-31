# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.



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
