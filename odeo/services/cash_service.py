from datetime import datetime

from odeo.models.list_transfers_response import ListTransfersResponse
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

        return ListTransfersResponse.from_json(response.json())

    @authenticated
    def create_va_topup(self, amount: int, user_id: int = None):
        params = {'amount': amount, 'user_id': user_id}
        response = self.request('POST', '/cash/va-topup', params)

        return self._raise_exception_on_error(response, lambda c: Topup.from_json(c))

    def find_active_va_topup(self, user_id: int = None):
        pass

    def cancel_va_topup(self, user_id: str = None):
        pass

    def get_balance(self, user_id: str = 'me'):
        pass

    def get_transactions(
            self,
            user_ids: list[str] = None,
            page_token: str = None,
            start_date: int = None,
            end_date: int = None
    ):
        pass
