from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Status(Enum):
    PENDING_DISBURSE_INQUIRY = 10000
    PENDING_DISBURSE_INQUIRY_DUE_TO_BANK_RECONCILIATION = 10002
    DISBURSEMENT_IS_ON_PROGRESS = 30000
    COMPLETED_DISBURSEMENT = 50000
    SUSPECT_DISBURSE_INQUIRY = 80000
    FAILED_DISBURSE_INQUIRY = 90000
    WRONG_BANK_ACCOUNT_NUMBER = 90001
    CLOSED_BANK_ACCOUNT = 90003
    INQUIRY_REJECTED_BY_THE_VENDOR_BANK = 90004
    INQUIRY_VENDOR_BANK_IS_DOWN = 90005


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
    status: Status
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
            status=Status(json.get('status')),
            created_at=created_at
        )
