from odeo.models.request import Request
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

    def list_transfers(
            self,
            reference_ids: list[str] = None,
            start_date: str = None,
            end_date: str = None,
            page_token: str = None
    ):
        pass

    def create_va_topup(self, amount: int, user_id: int = None):
        pass

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
