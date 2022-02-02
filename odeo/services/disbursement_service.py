import time

from odeo.api_signature import generate_signature
from odeo.models.bank import Bank
from odeo.services.base_service import BaseService


class DisbursementService(BaseService):

    def get_banks(self):
        self.request_access_token()

        path = '/dg/v1/banks'
        response = self._oauth.get(
            self._base_url + path,
            headers={'Accept': 'application/json'} | self._format_validation_headers(
                generate_signature(
                    'GET', path, '', self._oauth.access_token, int(time.time()), '', self._signing_key
                )
            )
        )
        content = response.json()

        if response.status_code != 200 or 'banks' not in content:
            return None

        return list(map(lambda bank: Bank.from_json(bank), content['banks']))

    def bank_account_inquiry(
            self,
            account_number: str,
            bank_id: int,
            customer_name: str,
            with_validation: bool = None
    ):
        pass

    def create_disbursement(
            self,
            account_number: str,
            amount: int,
            bank_id: int,
            customer_name: str,
            reference_id: str,
            description: str = None
    ):
        pass

    def get_disbursement(
            self, by_disbursement_id: int = None, by_reference_id: str = None
    ):
        pass
