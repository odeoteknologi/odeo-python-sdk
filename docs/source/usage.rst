Usage
=====

Installation
------------

The SDK currently supports Python 3.9 and later.

To use Odeo Python SDK, install the latest version using ``pip``:

.. code-block:: console
    
    pip install odeo-python-sdk

Basic Usage
-----------

First step to use the Odeo Python SDK you need to activate the OAuth setting, and the Payment Gateway & Disbursement access by following the guide on `Odeo For Business API Integration <https://docs.odeo.co.id/docs/integration/intro>`_ doc.

By following the guide you'll get your API credentials which consists of: ``client_id``, ``client_secret``, and ``signing_key``.

Next we create a new SDK ``Client`` object to access the various services API endpoint functions:

.. code-block:: python

    import odeo.client

    client = odeo.client.Client(
        client_id='…',
        client_secret='…',
        signing_key='…'
    )

After that we can access the API services with the cached property, e.g.: for accessing ``get_banks`` of Disbursement service:

.. code-block:: python

    banks = client.disbursement.get_banks()

By default, the client will access the development API server, to access production API server, set the ``base_url`` parameter to ``odeo.client.PRODUCTION_BASE_URL`` constant:

.. code-block:: python

    import odeo.client

    client = odeo.client.Client(
        client_id='…',
        client_secret='…',
        signing_key='…',
        base_url=odeo.client.PRODUCTION_BASE_URL
    )

How to access the endpoint functions of each API services, please see it's detailed API references:

- Disbursement service: :py:class:`odeo.services.disbursement.DisbursementService`
- Payment Gateway service: :py:class:`odeo.services.payment_gateway.PaymentGatewayService`
- Cash service: :py:class:`odeo.services.cash.CashService`
- Sub User service: :py:class:`odeo.services.sub_user.SubUserService`
