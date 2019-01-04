

class Spec(object):

    def __init__(self, name=None, links=None):
        self._name = name
        self._links = links

        if self._links:
            self._json = links['json']
            self._yaml = links['yaml']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, links):
        self._links = links

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, json):
        self._json = json

    @property
    def yaml(self):
        return self._yaml

    @yaml.setter
    def yaml(self, yaml):
        self._yaml = yaml
