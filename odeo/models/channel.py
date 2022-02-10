from dataclasses import dataclass


@dataclass
class Channel:
    fee: int | str
    channel_id: int
    pay_code: str
    amount: int
    total: int

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            fee=json.get('fee'),
            channel_id=json.get('channel_id'),
            pay_code=json.get('pay_code'),
            amount=json.get('amount'),
            total=json.get('total')
        )
