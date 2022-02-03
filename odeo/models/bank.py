from dataclasses import dataclass


@dataclass
class Bank:
    bank_id: int
    name: str
    bank_code: str
    swift_code: str

    @classmethod
    def from_json(cls, json):
        return Bank(
            bank_id=json.get('bank_id'),
            name=json.get('name'),
            bank_code=json.get('bank_code'),
            swift_code=json.get('swift_code')
        )
