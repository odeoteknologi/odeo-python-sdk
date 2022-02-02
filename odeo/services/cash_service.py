from odeo.models.request import Request
from odeo.services.base_service import BaseService


class CashService(BaseService):

    def create_bulk_transfers(self, requests: list[Request]):
        return

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
