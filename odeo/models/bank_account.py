from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Status(Enum):
    COMPLETED_INQUIRY = 50000
    FAILED_INQUIRY = 90000
    WRONG_BANK_ACCOUNT_NUMBER = 90001
    CLOSED_BANK_ACCOUNT = 90003
    INQUIRY_REJECTED_BY_THE_VENDOR_BANK = 90004
    INQUIRY_VENDOR_BANK_IS_DOWN = 90005


@dataclass
class BankAccount:
    bank_id: int
    account_number: str
    account_name: str
    customer_name: str
    fee: int
    status: Status
    created_at: datetime
    bank_account_inquiry_id: str
    validity: int

    @classmethod
    def from_json(cls, json):
        created_at = json.get('created_at')
        if created_at is not None:
            created_at = datetime.utcfromtimestamp(float(created_at))

        return BankAccount(
            bank_id=json.get('bank_id'),
            account_number=json.get('account_number'),
            account_name=json.get('account_name'),
            customer_name=json.get('customer_name'),
            fee=json.get('fee'),
            status=Status(json.get('status')),
            created_at=created_at,
            bank_account_inquiry_id=json.get('bank_account_inquiry_id'),
            validity=json.get('validity')
        )
