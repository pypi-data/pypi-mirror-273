import abc
import typing

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.services.services import EventEmitterMixin, EventLogger


class ImportTransactionsTransactionGater(abc.ABC):
    def __iter__(self) -> None:
        pass  # pragma: no cover


class ImportTransactionsAssetCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, asset_name: AssetName) -> Asset: ...  # pragma: no cover


EXPENSE_MADE = "expense_made"


class ImportTransactionsService(EventEmitterMixin):
    """
    Imports transactions from a source.
    """

    def __init__(
        self,
        transactions_gateway: ImportTransactionsTransactionGater,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ) -> None:
        self.transactions = transactions_gateway

        super().__init__(EXPENSE_MADE, event_log)

    def execute(self) -> None:
        for transaction in self.transactions:  # type: ignore
            if transaction.value > 0:
                continue  # Ignore income

            value = Money(int(str(transaction.value).replace(".", "")))

            date = transaction.date_of_movement.strftime("%Y-%m-%d")

            self.emit(
                value=int(value),  # type: ignore
                date_of=date,  # type: ignore
                description=transaction.description,  # type: ignore
            )
