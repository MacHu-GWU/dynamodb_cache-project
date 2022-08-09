# -*- coding: utf-8 -*-

"""

"""

import typing as T

import json
import dataclasses
from abc import ABC

from ..utils import utc_now
from ..abstract import AbstractCache


@dataclasses.dataclass
class InMemoryBackendRecord:
    """
    :param update_ts: last update timestamp
    """
    key: str
    value: bytes
    expire: int
    update_ts: int


in_memory_database: T.Dict[str, InMemoryBackendRecord] = dict()

VALUE = T.TypeVar("VALUE")  # represent a cached value, can be any object


class InMemoryBackend(
    ABC,
    T.Generic[VALUE],
):
    """
    Base in memory cache backend. You can customize the behavior by adding
    custom serializer / deserializer.
    """

    def _value_to_record(
        self,
        key: str,
        value: VALUE,
        expire: int = 0,
    ) -> InMemoryBackendRecord:
        return InMemoryBackendRecord(
            key=key,
            value=self._serialize(value),
            expire=expire,
            update_ts=int(utc_now().timestamp())
        )

    def _record_to_value(self, record: InMemoryBackendRecord) -> VALUE:
        return self._deserialize(record.value)

    def set(
        self,
        key: str,
        value: VALUE,
        expire: int = 0,
    ):
        """
        :param expire: Time-to-live in seconds
        """
        record = self._value_to_record(key, value, expire)
        in_memory_database[key] = record

    def get(
        self,
        key: str,
    ) -> T.Optional[VALUE]:
        try:
            record = in_memory_database[key]
        except KeyError:
            return None

        if record.expire:
            now = utc_now()
            if (
                (now.timestamp() - record.update_ts)
                < record.expire
            ):
                return self._record_to_value(record)
            else:
                return None
        else:
            return self._record_to_value(record)

    def clear(self):
        in_memory_database.clear()


class JsonDictInMemoryCache(
    InMemoryBackend[dict],
    AbstractCache[dict],
):
    """
    A built-in In memory cache designed to store JSON serializable dict.
    """

    def _serialize(self, value: dict) -> bytes:
        return json.dumps(value).encode("utf-8")

    def _deserialize(self, value: bytes) -> dict:
        return json.loads(value.decode("utf-8"))


class JsonListInMemoryCache(
    InMemoryBackend[list],
    AbstractCache[list],
):
    """
    A built-in In memory cache designed to store JSON serializable list.
    """

    def _serialize(self, value: list) -> bytes:
        return json.dumps(value).encode("utf-8")

    def _deserialize(self, value: bytes) -> list:
        return json.loads(value.decode("utf-8"))
