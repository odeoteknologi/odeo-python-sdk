API
===

Classes
--------------

.. autoclass:: odeo.client.Client
    :members:

.. autoclass:: odeo.services.disbursement.DisbursementService
    :members:

.. autoclass:: odeo.services.payment_gateway.PaymentGatewayService
    :members:

.. autoclass:: odeo.services.cash.CashService
    :members:

.. autoclass:: odeo.services.sub_user.SubUserService
    :members:

Data Classes
------------

.. automodule:: odeo.models.disbursement

    .. autoclass:: Bank
        :members:

    .. autoclass:: BankAccountStatus

    .. autoclass:: BankAccount
        :members:

    .. autoclass:: DisbursementStatus

    .. autoclass:: Disbursement
        :members:

.. automodule:: odeo.models.payment_gateway

    .. autoclass:: PaymentStatus

    .. autoclass:: Payment
        :members:

.. automodule:: odeo.models.cash

    .. autoclass:: Cash
        :members:

    .. autoclass:: Balance
        :members:

    .. autoclass:: Request
        :members:

    .. autoclass:: Channel
        :members:

    .. autoclass:: Topup
        :members:

    .. autoclass:: CashTransaction
        :members:

    .. autoclass:: TransactionsHistory
        :members:

    .. autoclass:: Transfer
        :members:

    .. autoclass:: TransfersList
        :members:

.. automodule:: odeo.models.sub_user

    .. autoclass:: SubUser
        :members:

    .. autoclass:: SubUsersList
        :members:

Exceptions
----------

.. automodule:: odeo.exceptions

    .. autoexception:: GeneralError
    .. autoexception:: InputValidationError
    .. autoexception:: InsufficientBalanceError
    .. autoexception:: InvalidBankError
    .. autoexception:: ResourceNotFoundError
