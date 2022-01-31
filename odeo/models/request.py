from dataclasses import dataclass


@dataclass
class Request:
    sender_user_id: int
    receiver_user_id: int
    amount: int
    reference_id: str
    note: str
