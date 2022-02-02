from odeo.exceptions.insufficient_balance_error import InsufficientBalanceError
from odeo.exceptions.invalid_bank_error import InvalidBankError
from odeo.models.bank import Bank
from odeo.models.bank_account import BankAccount
from odeo.services.base_service import BaseService


class DisbursementService(BaseService):

    def get_banks(self):
        self.request_access_token()

        response = self.request('GET', '/dg/v1/banks')
        content = response.json()

        if response.status_code != 200 or 'banks' not in content:
            return None

        return list(map(lambda bank: Bank.from_json(bank), content['banks']))

    def bank_account_inquiry(
            self,
            account_number: str,
            bank_id: int,
            customer_name: str,
            with_validation: bool = False
    ):
        self.request_access_token()

        response = self.request('POST', '/dg/v1/bank-account-inquiry', {
            'account_number': account_number,
            'bank_id': bank_id,
            'customer_name': customer_name,
            'with_validation': with_validation
        })
        content = response.json()

        if response.status_code == 400 and 'error_code' in content:
            if content['error_code'] == 40002:
                raise InvalidBankError(content['message'])
            elif content['error_code'] == 40011:
                raise InsufficientBalanceError(content['message'])
        elif response.status_code == 200:
            return BankAccount.from_json(response.json())

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
