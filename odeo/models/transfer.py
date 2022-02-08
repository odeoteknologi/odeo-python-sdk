from dataclasses import dataclass
from datetime import datetime

from odeo.models.request import _BaseRequest, _DefaultRequest


@dataclass
class _BaseTransfer:
    transfer_id: str
    created_at: datetime


@dataclass
class Transfer(_DefaultRequest, _BaseRequest, _BaseTransfer):

    @classmethod
    def from_json(cls, json: dict):
        created_at = json.get('created_at')
        if created_at is not None:
            created_at = datetime.utcfromtimestamp(float(created_at))

        return cls(
            transfer_id=json.get('transfer_id'),
            sender_user_id=json.get('sender_user_id'),
            receiver_user_id=json.get('receiver_user_id'),
            amount=json.get('amount'),
            reference_id=json.get('reference_id'),
            note=json.get('note'),
            created_at=created_at
        )
