from abc import ABC, abstractmethod
from .factory import Factory
from .serializable import Serializable
import numpy as np

class EmbeddingVector(Serializable):
    @property
    def vector(self):
        try:
            v = self._vdata
        except AttributeError:
            self._vdata = np.array([self._data])
            v = self._vdata
        return v

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return len(self._data)

    def __init__(self, data, model_name):
        self._data = data
        self.model_name = model_name

    def to_dict(self):
        return {
            'data': self.data,
            'model_name': self.model_name
        }

    @staticmethod
    def from_dict(data):
        assert len(data) == 2
        return EmbeddingVector(data=data['data'], model_name=data['model_name'])

class EmbeddingComputer(ABC):
    @property
    @abstractmethod
    def comparison_method(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def max_digest_size(self):
        raise NotImplemented()

    @abstractmethod
    def compute_tokens(self, text):
        raise NotImplemented()

    def check(self, text):
        return self.compute_tokens(text) <= self.max_digest_size

    @property
    @abstractmethod
    def max_digest_size(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def model_name(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def vector_size(self):
        raise NotImplemented()

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        # this returns an EmbeddingComputer object
        raise NotImplemented()

    @abstractmethod
    def get_embedding(self, text):
        # this returns a EmbeddingVector
        raise NotImplemented()


class EmbeddingComputerFactory(Factory):
    _class = EmbeddingComputer



