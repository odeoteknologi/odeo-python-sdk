import json
from datetime import datetime

from odeo.models.balance import Balance
from odeo.models.transactions_history import TransactionsHistory
from odeo.models.transfers_list import TransfersList
from odeo.models.request import Request
from odeo.models.topup import Topup
from odeo.models.transfer import Transfer
from odeo.services.base_service import BaseService, authenticated


class CashService(BaseService):

    @authenticated
    def create_bulk_transfers(self, requests: list[Request]):
        params = {'requests': (list(map(lambda request: request.to_dict(), requests)))}
        response = self.request('POST', '/cash/bulk-transfer', params)

        return self._raise_exception_on_error(
            response,
            lambda c: list(map(lambda transfer: Transfer.from_json(transfer), c['transfers']))
        )

    @authenticated
    def list_transfers(
            self,
            reference_ids: list[str] = None,
            start_date: datetime = None,
            end_date: datetime = None,
            page_token: str = None
    ):
        params = {}

        if reference_ids is not None:
            for i in range(0, len(reference_ids)):
                params[f'reference_ids[{i}]'] = reference_ids[i]
        if start_date is not None:
            params['start_date'] = int(start_date.timestamp())
        if end_date is not None:
            params['end_date'] = int(end_date.timestamp())
        if page_token is not None:
            params['page_token'] = page_token

        response = self.request('GET', '/cash/transfers', params)

        return TransfersList.from_json(response.json())

    @authenticated
    def create_va_topup(self, amount: int, user_id: int = None):
        params = {'amount': amount, 'user_id': user_id}
        response = self.request('POST', '/cash/va-topup', params)

        return self._raise_exception_on_error(response, lambda c: Topup.from_json(c))

    @authenticated
    def find_active_va_topup(self, user_id: int = None):
        params = {'user_id': user_id} if user_id is not None else {}
        response = self.request('GET', '/cash/va-topup/active', params)

        return self._raise_exception_on_error(response, lambda c: Topup.from_json(c))

    @authenticated
    def cancel_va_topup(self, user_id: str = None):
        params = {'user_id': user_id} if user_id is not None else None
        response = self.request('POST', '/cash/va-topup/cancel', params)

        return self._raise_exception_on_error(response, lambda c: c)

    @authenticated
    def get_balance(self, user_id: str = 'me'):
        response = self.request('GET', f'/cash/{user_id}/balance')

        return self._raise_exception_on_error(response, lambda c: Balance.from_json(c))

    @authenticated
    def get_transactions_history(
            self,
            user_ids: list[int] = None,
            start_date: int = None,
            end_date: int = None,
            page_token: str = None
    ):
        path = '/cash/transactions'
        params = {}

        if user_ids is not None:
            path = '/cash/sub-user-transactions'
            for i in range(0, len(user_ids)):
                params[f'user_ids[{i}]'] = user_ids[i]
        if start_date is not None:
            params['start_date'] = int(start_date.timestamp())
        if end_date is not None:
            params['end_date'] = int(end_date.timestamp())
        if page_token is not None:
            params['page_token'] = page_token

        response = self.request('GET', path, params)

        return TransactionsHistory.from_json(response.json())
