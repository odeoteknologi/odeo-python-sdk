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
        created_at = json.get('created_at')
        if created_at is not None:
            created_at = datetime.utcfromtimestamp(float(created_at))

        return BankAccount(
            bank_id=json.get('bank_id'),
            account_number=json.get('account_number'),
            account_name=json.get('account_name'),
            customer_name=json.get('customer_name'),
            fee=json.get('fee'),
            status=json.get('status'),
            created_at=created_at,
            bank_account_inquiry_id=json.get('bank_account_inquiry_id'),
            validity=json.get('validity')
        )
