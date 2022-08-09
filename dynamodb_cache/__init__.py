# -*- coding: utf-8 -*-

"""
A simple Dynamodb backed cache with TTL.
"""

from ._version import __version__

__short_description__ = "A simple Dynamodb backed cache with TTL."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

# public API
try:
    from .abstract import AbstractCache
    from .backend.in_memory import (
        InMemoryBackend,
        JsonDictInMemoryCache,
        JsonListInMemoryCache,
    )
    from .backend.dynamodb import (
        DynamodbBackendRecord as DynamodbTable,
        DynamodbBackend,
        JsonDictDynamodbCache,
        JsonListDynamodbCache,
    )
    from .multi_layer import (
        MultiLayerCache,
        JsonDictMultiLayerCache,
        JsonListMultiLayerCache,
    )
except ImportError as e:
    print(f"failed to import some module: {e}")
