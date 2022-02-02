from dataclasses import dataclass
from datetime import datetime


@dataclass
class BankAccount:
    bank_id: int
    account_number: str
    account_name: str
    customer_name: str
    fee: int
    status: int
    created_at: datetime
    bank_account_inquiry_id: str
    validity: int

    @classmethod
    def from_json(cls, json):
        return BankAccount(
            bank_id=json['bank_id'],
            account_number=json['account_number'],
            account_name=json['account_name'],
            customer_name=json['customer_name'],
            fee=json['fee'],
            status=json['status'],
            created_at=datetime.utcfromtimestamp(float(json['created_at'])),
            bank_account_inquiry_id=json['bank_account_inquiry_id'],
            validity=json['validity']
        )
