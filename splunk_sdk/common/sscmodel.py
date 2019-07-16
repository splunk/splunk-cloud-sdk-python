import json
from abc import ABC, abstractmethod
import datetime
from typing import Optional

from requests import Request, Response


class SSCModel(ABC):
    """
    Base class for all SSC model objects. Allow access to raw response and handle the serialization
    and deserialization of the model objects.
    """

    def __init__(self):
        self._response = None

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @property
    def response(self) -> Optional[Response]:
        """
        :return: the raw HTTP response from the service call. Will return None if the model was not created from a call.
        """
        return self._response

    @response.setter
    def response(self, response: Response):
        self._response = response

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=lambda o: o.to_dict())

    def _parse_date(self, datestr: datetime):
        return datestr

    def to_str(self):
        """Returns the string representation of the model"""
        return self.to_json()

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, self.__class__):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    def reprJSON(self):
        return self.to_dict()


class SSCVoidModel(SSCModel):
    """
    SSCVoidModel is here simply to allow access to the underlying raw response if needed.
    """

    def __init__(self, response: Response):
        self._response = response

    def to_dict(self) -> dict:
        return {}
