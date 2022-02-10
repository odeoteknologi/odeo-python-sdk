from dataclasses import dataclass

from odeo.models.transfer import Transfer


@dataclass
class ListTransfersResponse:
    transfers: list[Transfer]
    next_page_token: str = None

    @classmethod
    def from_json(cls, json: dict):
        if 'transfers' in json:
            transfers = list(map(lambda t: Transfer.from_json(t), json.get('transfers')))

            return cls(
                transfers=transfers,
                next_page_token=json.get('next_page_token') if 'next_page_token' in json else None
            )
