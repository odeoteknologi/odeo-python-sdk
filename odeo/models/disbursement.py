from dataclasses import dataclass
from datetime import datetime


@dataclass
class Disbursement:
    disbursement_id: str
    bank_id: int
    bank_code: str
    account_number: str
    customer_name: str
    amount: int
    fee: int
    description: str | None
    reference_id: str
    status: int
    created_at: datetime

    @classmethod
    def from_json(cls, json: dict):
        created_at = json.get('created_at')
        if created_at is not None:
            created_at = datetime.utcfromtimestamp(float(created_at))

        return Disbursement(
            disbursement_id=json.get('disbursement_id'),
            bank_id=json.get('bank_id'),
            bank_code=json.get('bank_code'),
            account_number=json.get('account_number'),
            customer_name=json.get('customer_name'),
            amount=json.get('amount'),
            fee=json.get('fee'),
            description=json.get('description'),
            reference_id=json.get('reference_id'),
            status=json.get('status'),
            created_at=created_at
        )
