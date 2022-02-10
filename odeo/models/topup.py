from dataclasses import dataclass
from datetime import datetime

from odeo.models.channel import Channel


@dataclass
class Topup:
    channels: list[Channel]
    topup_id: str
    expires_at: datetime

    @classmethod
    def from_json(cls, json: dict):
        expires_at = json.get('expires_at')
        if expires_at is not None:
            expires_at = datetime.utcfromtimestamp(float(expires_at))

        return cls(
            channels=list(map(lambda c: Channel.from_json(c), json.get('channels'))),
            topup_id=json.get('topup_id'),
            expires_at=expires_at
        )
