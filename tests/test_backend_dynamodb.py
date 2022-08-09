# -*- coding: utf-8 -*-

import os
import time
import pytest

import json
import dataclasses

import pynamodb.models

from dynamodb_cache.abstract import AbstractCache
from dynamodb_cache.backend.dynamodb import (
    DynamodbBackendRecord,
    DynamodbBackend,
    JsonDictDynamodbCache,
    JsonListDynamodbCache,
)


@dataclasses.dataclass
class Credential:
    username: str
    password: str


class CredentialCache(
    DynamodbBackend[Credential],
    AbstractCache[Credential],
):
    def _serialize(self, value: Credential) -> bytes:
        return json.dumps(dataclasses.asdict(value)).encode("utf-8")

    def _deserialize(self, value: bytes) -> Credential:
        return Credential(**json.loads(value.decode("utf-8")))


class DynamodbTable(DynamodbBackendRecord):
    class Meta:
        table_name = f"dynamodb-cache"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE


# DynamodbTable.create_table(wait=True)

@pytest.mark.parametrize(
    "cache",
    [
        CredentialCache(DynamodbTable),
    ]
)
def test_backend(cache: AbstractCache):
    cache.clear()

    alice_credential = Credential(username="alice", password="123456")
    cache.set("alice", alice_credential)
    assert cache.get("alice").password == "123456"

    assert cache.get("bob") is None

    cache.set("alice", alice_credential, expire=1)
    assert cache.get("alice").password == "123456"

    time.sleep(2)
    assert cache.get("alice") is None


@pytest.mark.parametrize(
    "cache,data",
    [
        (
            JsonDictDynamodbCache(DynamodbTable),
            {"a": 1}
        ),
        (
            JsonListDynamodbCache(DynamodbTable),
            [1, 2, 3]
        )
    ]
)
def test_in_memory_cache(cache: DynamodbBackend, data):
    cache.set("key", data)
    assert cache.get("key") == data


if __name__ == "__main__":
    import sys
    import subprocess

    abspath = os.path.abspath(__file__)
    dir_project_root = os.path.dirname(abspath)
    for _ in range(10):
        if os.path.exists(os.path.join(dir_project_root, ".git")):
            break
        else:
            dir_project_root = os.path.dirname(dir_project_root)
    else:
        raise FileNotFoundError("cannot find project root dir!")
    dir_htmlcov = os.path.join(dir_project_root, "htmlcov")
    bin_pytest = os.path.join(os.path.dirname(sys.executable), "pytest")

    args = [
        bin_pytest,
        "-s", "--tb=native",
        f"--rootdir={dir_project_root}",
        "--cov=dynamodb_cache.backend.dynamodb",
        "--cov-report", "term-missing",
        "--cov-report", f"html:{dir_htmlcov}",
        abspath,
    ]
    subprocess.run(args)
