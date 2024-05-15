import abc
import typing
from datetime import datetime

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
EXPENSES_IMPORTED = "expenses_imported"


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

        super().__init__(EXPENSES_IMPORTED, event_log)

    def execute(self) -> None:

        last_imported_date = None
        for event in self._event_log:  # type: ignore
            if event.name != EXPENSES_IMPORTED:
                continue

            last_imported_date = datetime.strptime(
                event.data.get("last_seen_expense"), "%Y-%m-%d"
            )

        expense_dates = []
        expense_date = None
        for transaction in self.transactions:  # type: ignore
            if (
                last_imported_date
                and last_imported_date >= transaction.date_of_movement
            ):
                continue

            if transaction.value > 0:
                continue  # Ignore income

            expense_dates.append(transaction.date_of_movement)
            expense_date = transaction.date_of_movement.strftime("%Y-%m-%d")

            value = Money(int(str(transaction.value).replace(".", "")))

            self.emit(
                event_name=EXPENSE_MADE,
                value=int(value),  # type: ignore
                date_of=expense_date,  # type: ignore
                description=transaction.description,  # type: ignore
            )

        if not expense_date:
            return

        self.emit(last_seen_expense=sorted(expense_dates)[-1].strftime("%Y-%m-%d"))
