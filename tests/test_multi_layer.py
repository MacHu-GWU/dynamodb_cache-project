# -*- coding: utf-8 -*-

import os
import time
import pytest

import json
import dataclasses

import pynamodb.models

from dynamodb_cache.abstract import AbstractCache
from dynamodb_cache.backend.in_memory import (
    JsonDictInMemoryCache,
    JsonListInMemoryCache,
)
from dynamodb_cache.backend.dynamodb import (
    DynamodbBackendRecord,
    JsonDictDynamodbCache,
    JsonListDynamodbCache,
)
from dynamodb_cache.multi_layer import (
    MultiLayerCache,
    JsonDictMultiLayerCache,
    JsonListMultiLayerCache,
)


class DynamodbTable(DynamodbBackendRecord):
    class Meta:
        table_name = f"dynamodb-cache"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE


@pytest.mark.skipif("CI" in os.environ)
@pytest.mark.parametrize(
    "cache,data",
    [
        (
            JsonDictMultiLayerCache([
                JsonDictInMemoryCache(),
                JsonDictDynamodbCache(DynamodbTable),
            ]),
            {"a": 1}
        ),
        (
            JsonListMultiLayerCache([
                JsonListInMemoryCache(),
                JsonListDynamodbCache(DynamodbTable),
            ]),
            [1, 2, 3]
        )
    ]
)
def test_in_memory_cache(cache: MultiLayerCache, data):
    cache.set("key", data)
    assert cache.get("key") == data
    assert cache.get("invalid") is None


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
        "--cov=dynamodb_cache.multi_layer",
        "--cov-report", "term-missing",
        "--cov-report", f"html:{dir_htmlcov}",
        abspath,
    ]
    subprocess.run(args)
