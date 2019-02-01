# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.


class Health(object):

    def __init__(self, status):
        self._status = status

    @property
    def status(self):
        """Return the status of the KVStore API"""
        return self._status

    @status.setter
    def status(self, status):
        """Set the status of the KVStore API"""
        self._status = status
