from dataclasses import dataclass


@dataclass
class Cash:
    amount: int
    currency: str
    formatted_amount: str

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            amount=json.get('amount'),
            currency=json.get('currency'),
            formatted_amount=json.get('formatted_amount')
        )


@dataclass
class Balance:
    cash: Cash
    locked_cash: Cash

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            cash=Cash.from_json(json.get('cash')),
            locked_cash=Cash.from_json(json.get('locked_cash'))
        )
