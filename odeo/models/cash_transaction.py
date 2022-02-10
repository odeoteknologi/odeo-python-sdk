from dataclasses import dataclass
from datetime import datetime


@dataclass
class CashTransaction:
    cash_transaction_id: str
    user_id: str
    amount: int
    balance_before: int
    balance_after: int
    transaction_type: str
    created_at: datetime

    @classmethod
    def from_json(cls, json: dict):
        created_at = json.get('created_at')
        if created_at is not None:
            created_at = datetime.utcfromtimestamp(float(created_at))

        return cls(
            cash_transaction_id=json.get('cash_transaction_id'),
            user_id=json.get('user_id'),
            amount=json.get('amount'),
            balance_before=json.get('balance_before'),
            balance_after=json.get('balance_after'),
            transaction_type=json.get('transaction_type'),
            created_at=created_at
        )
