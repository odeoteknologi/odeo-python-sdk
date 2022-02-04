from dataclasses import dataclass


@dataclass
class SubUser:
    user_id: int
    name: str
    phone_number: str
    email: str

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            user_id=json.get('user_id'),
            name=json.get('name'),
            phone_number=json.get('phone_number'),
            email=json.get('email')
        )
