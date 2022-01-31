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
            bank_id=json['bank_id'],
            name=json['name'],
            bank_code=json['bank_code'],
            swift_code=json['swift_code']
        )
