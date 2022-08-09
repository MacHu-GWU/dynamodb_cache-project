.. _release_history:

Release and Version History
==============================================================================


0.1.2 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.1 (2022-08-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Features and Improvements**

- First Release
- Provide a simple base in-memory cache, Dynamodb-backed cache and multi-layer cache. Users can implement their own serializer to meet their requirements.
- Additional built-in cache backend provided.
    - ``InMemoryBackend``
    - ``JsonDictInMemoryCache``
    - ``JsonListInMemoryCache``
    - ``DynamodbBackend``
    - ``JsonDictDynamodbCache``
    - ``JsonListDynamodbCache``
    - ``MultiLayerCache``
    - ``JsonDictMultiLayerCache``
    - ``JsonListMultiLayerCache``
