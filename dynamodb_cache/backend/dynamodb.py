# -*- coding: utf-8 -*-

import typing as T
import json

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    BinaryAttribute,
    NumberAttribute,
)

from abc import ABC

from ..utils import utc_now
from ..abstract import AbstractCache


class DynamodbBackendRecord(Model):
    """
    The Dynamodb table backend for :class:`DynamodbCache`.
    """
    key: str = UnicodeAttribute(hash_key=True)
    value: bytes = BinaryAttribute()
    expire: int = NumberAttribute()
    update_ts: int = NumberAttribute()

    @classmethod
    def delete_all(cls) -> int:
        ith = 0
        with cls.batch_write() as batch:
            for ith, item in enumerate(cls.scan(), start=1):
                batch.delete(item)
        return ith


VALUE = T.TypeVar("VALUE")  # represent a cached value, can be any object


class DynamodbBackend(
    ABC,
    T.Generic[VALUE],
):
    def __init__(self, pynamodb_table: T.Type[DynamodbBackendRecord]):
        self.pynamodb_table = pynamodb_table

    def _value_to_record(
        self,
        key: str,
        value: VALUE,
        expire: int = 0,
    ) -> DynamodbBackendRecord:
        return self.pynamodb_table(
            key=key,
            value=self._serialize(value),
            expire=expire,
            update_ts=int(utc_now().timestamp())
        )

    def _record_to_value(self, record: DynamodbBackendRecord) -> VALUE:
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
        record.save()

    def get(
        self,
        key: str,
    ) -> T.Optional[VALUE]:
        try:
            record = self.pynamodb_table.get(key)
        except self.pynamodb_table.DoesNotExist:
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
        self.pynamodb_table.delete_all()


class JsonDictDynamodbCache(
    DynamodbBackend[dict],
    AbstractCache[dict],
):
    def _serialize(self, value: dict) -> bytes:
        return json.dumps(value).encode("utf-8")

    def _deserialize(self, value: bytes) -> dict:
        return json.loads(value.decode("utf-8"))


class JsonListDynamodbCache(
    DynamodbBackend[list],
    AbstractCache[list],
):
    def _serialize(self, value: list) -> bytes:
        return json.dumps(value).encode("utf-8")

    def _deserialize(self, value: bytes) -> list:
        return json.loads(value.decode("utf-8"))
