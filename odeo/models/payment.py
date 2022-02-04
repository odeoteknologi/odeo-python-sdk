from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    PAYMENT_VERIFICATION_IS_ON_PROGRESS = 30000
    PAYMENT_IS_COMPLETED_OR_PAID = 50000
    SUSPECT_PAYMENT = 80000
    FAILED_PAYMENT = 90000
    PAYMENT_FAILED_REJECTED_BY_MERCHANT = 90001


@dataclass
class Payment:
    payment_id: int
    amount: int
    fee: int
    status: Status
    reference_id: str

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            payment_id=json.get('payment_id'),
            amount=json.get('amount'),
            fee=json.get('fee'),
            status=Status(json.get('status')),
            reference_id=json.get('reference_id')
        )
