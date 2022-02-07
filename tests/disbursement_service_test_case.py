import json
import unittest
from datetime import datetime

import odeo.client
from odeo.exceptions.insufficient_balance_error import InsufficientBalanceError
from odeo.exceptions.invalid_bank_error import InvalidBankError
from odeo.exceptions.resourse_not_found_error import ResourceNotFoundError
from odeo.models.bank import Bank
from odeo.models.bank_account import BankAccount, Status as BankAccountStatus
from odeo.models.disbursement import Disbursement, Status as DisbursementStatus
from tests.service_test_case import ServiceTestCase


class DisbursementServiceTestCase(ServiceTestCase):

    def test_get_banks(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/banks',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'UxTAo4TnY4sMUX3kUMPJSRD7pYwP73UJ6wmJArXFyRs='
            },
            text=json.dumps({
                'banks': [{
                    'bank_id': 1,
                    'name': 'BCA',
                    'bank_code': '014',
                    'swift_code': 'CENAIDJA'
                }]
            })
        )

        self.assertEqual(
            [Bank(bank_id=1, name='BCA', bank_code='014', swift_code='CENAIDJA')],
            self.client.disbursement.get_banks()
        )

    def test_get_banks_failed(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/banks',
            status_code=400,
            text=json.dumps({
                'message': 'Test error message',
                'status_code': 400,
                'error_code': 10000
            })
        )

        self.assertIsNone(self.client.disbursement.get_banks())

    def test_bank_account_inquiry(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/bank-account-inquiry',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'xXZNi3mjrdmp6NM6drpXFyTcZGec4b4dxuA5dB/cHqI='
            },
            text=json.dumps({
                'bank_id': 1,
                'account_number': '1234567890',
                'account_name': 'Agus Hartono',
                'customer_name': 'Agus Hartono',
                'fee': 1000,
                'status': 50000,
                'created_at': '1612137600',
                'bank_account_inquiry_id': '123',
                'validity': 100
            })
        )

        self.assertEqual(
            BankAccount(
                1,
                '1234567890',
                'Agus Hartono',
                'Agus Hartono',
                1000,
                BankAccountStatus.COMPLETED_INQUIRY,
                datetime(2021, 2, 1),
                '123',
                100
            ),
            self.client.disbursement.bank_account_inquiry(
                '1234567890', 1, 'Agus Hartono', True
            )
        )

    def test_bank_account_inquiry_failed_invalid_bank(self):
        self._create_failed_bank_account_inquiry_test(
            InvalidBankError, 40002, 'Unknown error: INVALID BANK'
        )

    def test_bank_account_inquiry_failed_insufficient_balance(self):
        self._create_failed_bank_account_inquiry_test(
            InsufficientBalanceError, 40011, 'Unknown error: INSUFFICIENT BALANCE'
        )

    def _create_failed_bank_account_inquiry_test(self, error, error_code, message):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/bank-account-inquiry',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'xXZNi3mjrdmp6NM6drpXFyTcZGec4b4dxuA5dB/cHqI='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': error_code
            })
        )
        with self.assertRaises(error) as ctx:
            self.client.disbursement.bank_account_inquiry(
                '1234567890', 1, 'Agus Hartono', True
            )
        self.assertEqual(str(ctx.exception), message)
        self.assertEqual(ctx.exception.error_code, error_code)

    def test_create_disbursement(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/disbursements',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'YrWxeSVGG8/Hn2zMGWfzuNutW5UNJMLyXlsDBQFlWfQ='
            },
            text=json.dumps({
                'disbursement_id': '123',
                'bank_id': 1,
                'bank_code': '014',
                'account_number': '1234567890',
                'customer_name': 'Agus Hartono',
                'amount': 1000000,
                'fee': 5000,
                'description': 'Example fund disbursement',
                'reference_id': 'EXAMPLE-REF-ID-001',
                'status': 10000,
                'created_at': '1612137600'
            })
        )

        self.assertEqual(
            Disbursement(
                '123',
                1,
                '014',
                '1234567890',
                'Agus Hartono',
                1000000,
                5000,
                'Example fund disbursement',
                'EXAMPLE-REF-ID-001',
                DisbursementStatus.PENDING_DISBURSE_INQUIRY,
                datetime(2021, 2, 1)
            ),
            self.client.disbursement.create_disbursement(
                '1234567890',
                1000000,
                1,
                'Agus Hartono',
                'EXAMPLE-REF-ID-001',
                'Example fund disbursement'
            )
        )

    def test_create_disbursement_without_description(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/disbursements',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'JmIv/2S7NyOotzi3dGYrhW7Qc8Mat3GU5ANcW8/qumA='
            },
            text=json.dumps({
                'disbursement_id': '123',
                'bank_id': 1,
                'bank_code': '014',
                'account_number': '1234567890',
                'customer_name': 'Agus Hartono',
                'amount': 1000000,
                'fee': 5000,
                # 'description': '',
                'reference_id': 'EXAMPLE-REF-ID-001',
                'status': 10000,
                'created_at': '1612137600'
            })
        )

        self.assertEqual(
            Disbursement(
                '123',
                1,
                '014',
                '1234567890',
                'Agus Hartono',
                1000000,
                5000,
                None,
                'EXAMPLE-REF-ID-001',
                DisbursementStatus.PENDING_DISBURSE_INQUIRY,
                datetime(2021, 2, 1)
            ),
            self.client.disbursement.create_disbursement(
                '1234567890',
                1000000,
                1,
                'Agus Hartono',
                'EXAMPLE-REF-ID-001'
            )
        )

    def test_create_disbursement_failed_invalid_bank(self):
        self._create_failed_create_disbursements_test(
            InvalidBankError, 40002, 'Unknown error: INVALID BANK'
        )

    def test_create_disbursement_failed_insufficient_balance(self):
        self._create_failed_create_disbursements_test(
            InsufficientBalanceError, 40011, 'Unknown error: INSUFFICIENT BALANCE'
        )

    def _create_failed_create_disbursements_test(self, error, error_code, message):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/disbursements',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'YrWxeSVGG8/Hn2zMGWfzuNutW5UNJMLyXlsDBQFlWfQ='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': error_code
            })
        )
        with self.assertRaises(error) as ctx:
            self.client.disbursement.create_disbursement(
                '1234567890',
                1000000,
                1,
                'Agus Hartono',
                'EXAMPLE-REF-ID-001',
                'Example fund disbursement'
            )
        self.assertEqual(str(ctx.exception), message)
        self.assertEqual(ctx.exception.error_code, error_code)

    def test_get_disbursement_by_disbursement_id(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/disbursements/123',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'Ds7dqFQTYcpY176I+hk1Vwi4fC6kYyNYBo4CsIsIZB4='
            },
            text=json.dumps({
                'disbursement_id': '123',
                'bank_id': 1,
                'bank_code': '014',
                'account_number': '1234567890',
                'customer_name': 'Agus Hartono',
                'amount': 1000000,
                'fee': 5000,
                'description': 'Example fund disbursement',
                'reference_id': 'EXAMPLE-REF-ID-001',
                'status': 10000,
                'created_at': '1612137600'
            })
        )

        self.assertEqual(
            Disbursement(
                '123',
                1,
                '014',
                '1234567890',
                'Agus Hartono',
                1000000,
                5000,
                'Example fund disbursement',
                'EXAMPLE-REF-ID-001',
                DisbursementStatus.PENDING_DISBURSE_INQUIRY,
                datetime(2021, 2, 1)
            ),
            self.client.disbursement.get_disbursement(by_disbursement_id=123)
        )

    def test_get_disbursement_by_disbursement_id_failed_not_exist(self):
        self._create_failed_get_disbursement_test(
            '/dg/v1/disbursements/123',
            'Ds7dqFQTYcpY176I+hk1Vwi4fC6kYyNYBo4CsIsIZB4=',
            lambda: self.client.disbursement.get_disbursement(by_disbursement_id=123)
        )

    def _create_failed_get_disbursement_test(self, path, signature, callback):
        message = 'Disbursement not found'
        error_code = 20002
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + path,
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': signature
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': error_code
            })
        )
        with self.assertRaises(ResourceNotFoundError) as ctx:
            callback()
        self.assertEqual(str(ctx.exception), message)
        self.assertEqual(ctx.exception.error_code, error_code)

    def test_get_disbursement_by_reference_id(self):
        path = '/dg/v1/disbursements/reference-id/EXAMPLE-REF-ID-001'
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + path,
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'bS1/9owpQa5eIisCNMZ+E4c7n/XXx7P5fvh9DQ40+gk='
            },
            text=json.dumps({
                'disbursement_id': '123',
                'bank_id': 1,
                'bank_code': '014',
                'account_number': '1234567890',
                'customer_name': 'Agus Hartono',
                'amount': 1000000,
                'fee': 5000,
                'description': 'Example fund disbursement',
                'reference_id': 'EXAMPLE-REF-ID-001',
                'status': 10000,
                'created_at': '1612137600'
            })
        )

        self.assertEqual(
            Disbursement(
                '123',
                1,
                '014',
                '1234567890',
                'Agus Hartono',
                1000000,
                5000,
                'Example fund disbursement',
                'EXAMPLE-REF-ID-001',
                DisbursementStatus.PENDING_DISBURSE_INQUIRY,
                datetime(2021, 2, 1)
            ),
            self.client.disbursement.get_disbursement(by_reference_id='EXAMPLE-REF-ID-001')
        )

    def test_get_disbursement_by_reference_id_failed_disbursement_not_found(self):
        self._create_failed_get_disbursement_test(
            '/dg/v1/disbursements/reference-id/EXAMPLE-REF-ID-001',
            'bS1/9owpQa5eIisCNMZ+E4c7n/XXx7P5fvh9DQ40+gk=',
            lambda: self.client.disbursement.get_disbursement(by_reference_id='EXAMPLE-REF-ID-001')
        )

    def test_get_disbursement_mutually_exclusive_parameters(self):
        with self.assertRaises(AssertionError):
            self.client.disbursement.get_disbursement()

        with self.assertRaises(AssertionError):
            self.client.disbursement.get_disbursement(by_disbursement_id=123, by_reference_id='123')


if __name__ == '__main__':
    unittest.main()
