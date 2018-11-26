class Health(object):

    def __init__(self, status):
        self._status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
