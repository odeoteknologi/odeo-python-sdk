import dataclasses
from dataclasses import dataclass


@dataclass
class _BaseRequest:
    receiver_user_id: int | str
    amount: int
    reference_id: str


@dataclass
class _DefaultRequest:
    sender_user_id: int | str = None
    note: str = None


@dataclass
class Request(_DefaultRequest, _BaseRequest):

    def to_dict(self):
        return dataclasses.asdict(self)
