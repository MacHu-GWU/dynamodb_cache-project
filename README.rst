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

TODO: add usage doc

.. _install:

Install
------------------------------------------------------------------------------

``dynamodb_cache`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install dynamodb_cache

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade dynamodb_cache