# -*- coding: utf-8 -*-

"""

"""

import typing as T
from abc import ABC, abstractmethod

VALUE = T.TypeVar("VALUE")  # represent a cached value, can be any object


class AbstractCache(
    ABC,
    T.Generic[VALUE],
):
    """
    An abstract cache class regardless of the backend.
    """

    @abstractmethod
    def _serialize(self, value: VALUE) -> bytes:
        """
        Abstract serialization function using binary protocol.
        """
        raise NotImplementedError

    @abstractmethod
    def _deserialize(self, value: bytes) -> VALUE:
        """
        Abstract deserialization function using binary protocol.
        """
        raise NotImplementedError

    def set(
        self,
        key: str,
        value: VALUE,
        expire: int = 0,
    ):
        """
        Store object in cache.

        :param key: cache key
        :param value: the object you stored in cache
        :param expire: Time-to-live in seconds
        """
        raise NotImplementedError

    def get(
        self,
        key: str,
    ) -> T.Optional[VALUE]:
        """
        Get object from cache.

        :param key: cache key
        :return:
        """
        raise NotImplementedError

    def clear(self):
        """
        Disable all records in cache.
        """
        raise NotImplementedError
