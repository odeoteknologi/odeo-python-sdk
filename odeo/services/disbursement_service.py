from odeo.exceptions.insufficient_balance_error import InsufficientBalanceError
from odeo.exceptions.invalid_bank_error import InvalidBankError
from odeo.models.bank import Bank
from odeo.models.bank_account import BankAccount
from odeo.models.disbursement import Disbursement
from odeo.services.base_service import BaseService, authenticated


class DisbursementService(BaseService):

    @authenticated
    def get_banks(self):
        response = self.request('GET', '/dg/v1/banks')
        content = response.json()

        if response.status_code == 200 and 'banks' in content:
            return list(map(lambda bank: Bank.from_json(bank), content['banks']))

    @authenticated
    def bank_account_inquiry(
            self,
            account_number: str,
            bank_id: int,
            customer_name: str,
            with_validation: bool = False
    ):
        response = self.request('POST', '/dg/v1/bank-account-inquiry', {
            'account_number': account_number,
            'bank_id': bank_id,
            'customer_name': customer_name,
            'with_validation': with_validation
        })

        return self._raise_exception_on_error(
            response.json(), response, lambda c: BankAccount.from_json(c)
        )

    @staticmethod
    def _raise_exception_on_error(content, response, success: callable):
        if response.status_code == 400 and 'error_code' in content:
            if content['error_code'] == 40002:
                raise InvalidBankError(content['message'])
            elif content['error_code'] == 40011:
                raise InsufficientBalanceError(content['message'])
        elif response.status_code == 200:
            return success(content)

    @authenticated
    def create_disbursement(
            self,
            account_number: str,
            amount: int,
            bank_id: int,
            customer_name: str,
            reference_id: str,
            description: str = None
    ):
        params = {
            'account_number': account_number,
            'amount': amount,
            'bank_id': bank_id,
            'customer_name': customer_name,
            'reference_id': reference_id
        }
        if description is not None:
            params['description'] = description

        response = self.request('POST', '/dg/v1/disbursements', params)

        return self._raise_exception_on_error(
            response.json(), response, lambda c: Disbursement.from_json(c)
        )

    @authenticated
    def get_disbursement(
            self, by_disbursement_id: int = None, by_reference_id: str = None
    ):
        pass
