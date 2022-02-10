from dataclasses import dataclass

from odeo.models.cash_transaction import CashTransaction


@dataclass
class TransactionsHistory:
    cash_transactions: list[CashTransaction]
    next_page_token: str = None

    @classmethod
    def from_json(cls, json: dict):
        if 'cash_transactions' in json:
            cash_transactions = list(
                map(lambda c: CashTransaction.from_json(c), json.get('cash_transactions'))
            )

            return cls(
                cash_transactions=cash_transactions,
                next_page_token=json.get('next_page_token') if 'next_page_token' in json else None
            )
