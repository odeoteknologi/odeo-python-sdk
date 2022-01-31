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
        ).json()

        return list(map(lambda bank: Bank.from_json(bank), response['banks']))
