.. image:: https://github.com/MacHu-GWU/dynamodb_cache-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/dynamodb_cache-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/dynamodb_cache-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/dynamodb_cache-project

.. image:: https://img.shields.io/pypi/v/dynamodb_cache.svg
    :target: https://pypi.python.org/pypi/dynamodb_cache

.. image:: https://img.shields.io/pypi/l/dynamodb_cache.svg
    :target: https://pypi.python.org/pypi/dynamodb_cache

.. image:: https://img.shields.io/pypi/pyversions/dynamodb_cache.svg
    :target: https://pypi.python.org/pypi/dynamodb_cache

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/dynamodb_cache-project

------

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://dynamodb_cache.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/dynamodb_cache-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/dynamodb_cache-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/dynamodb_cache-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/dynamodb_cache#files


Welcome to ``dynamodb_cache`` Documentation
==============================================================================
Redis is a good distributive cache. What if I don't want to manage a server? AWS Dynamodb could be another awesome backend for distributive cache. Reasons are:

- It takes 5 seconds to create a backend table
- No server to manage
- It automatically scale up and down
- The pricing can be pay-as-you-go
- It can handle 1K + concurrent read easily

**Usage**

.. code-block:: python

    # -*- coding: utf-8 -*-

    """
    Code example of using ``dynamodb_cache`` library to create your custom cache
    """

    import json
    import dataclasses

    import pynamodb.models
    from dynamodb_cache import (
        AbstractCache,
        DynamodbTable,
        DynamodbBackend,
    )


    # You have a logic to read database credential from AWS Secret Manager
    # you would like to cache it for 1 hour and don't want to invoke
    # AWS Secret Manager API during that hour.
    # The database credential is a custom object
    @dataclasses.dataclass
    class DatabaseCredential:
        host: str
        port: int
        database: str
        username: str
        password: str


    def get_credential_from_aws_secret_manager() -> DatabaseCredential:
        print("read credential from aws secret manager")
        return DatabaseCredential(
            host="www.db.com",
            port=5432,
            database="my_database",
            username="alice",
            password="123456",
        )


    # First you need to define a DynamodbTable for use
    # just give it a name, and the PAY_PER_REQUEST_BILLING_MODE can keep your cost
    # ver low (<= $1 per month) at begin
    # We use PynamoDB library to create a simple ORM layer
    class MyDynamodbTable(DynamodbTable):
        class Meta:
            table_name = f"dynamodb-cache"
            region = "us-east-1"
            billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE


    MyDynamodbTable.create_table(wait=True)


    # Define your custom cache to use Dynamodb as backend
    # define your own serialization function to convert your object to binary
    #
    # **NOTE**:
    #
    # 1. put the DynamodbBackend FIRST in your inheritance
    # 2. Use TypeHint syntax to tell your custom cache what is the return type

    class DatabaseCredentialCache(
        DynamodbBackend[DatabaseCredential],
        AbstractCache[DatabaseCredential],
    ):
        def _serialize(self, value: DatabaseCredential) -> bytes:
            return json.dumps(dataclasses.asdict(value)).encode("utf-8")

        def _deserialize(self, value: bytes) -> DatabaseCredential:
            return DatabaseCredential(**json.loads(value.decode("utf-8")))


    # Then create an instance of your custom cache
    database_credential_cache = DatabaseCredentialCache(MyDynamodbTable)


    # Last, wrap your real "get_credential_from_aws_secret_manager" function
    # use cache when possible
    def get_credential():
        key = "my_db_credential"
        database_credential = database_credential_cache.get(key)
        if database_credential is None:
            database_credential = get_credential_from_aws_secret_manager()
            database_credential_cache.set(key, database_credential, expire=3600)
        return database_credential


    # **NOW**, you can just use "get_credential()" function to get the credential
    # preferably from cache
    # you will see "read credential from aws secret manager" ONLY once
    print(get_credential())
    print(get_credential())


.. _install:

Install
------------------------------------------------------------------------------

``dynamodb_cache`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install dynamodb_cache

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade dynamodb_cache