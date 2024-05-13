import typing
from datetime import datetime
from typing import Any

import pastperfect

from profitpulse.data.data import View
from profitpulse.services.import_transactions import EXPENSE_MADE


class ExpensesView(View):
    def __init__(
        self,
        session: typing.Any,
        seller: typing.Optional[str] = None,
        group_seller: typing.Optional[bool] = False,
        since: typing.Optional[datetime] = None,
        until: typing.Optional[datetime] = None,
    ):
        self._session = session
        self._seller = seller
        self._group_seller = group_seller
        self._since = since
        self._until = until

    @property
    def data(self) -> Any:  # noqa
        events = pastperfect.Events(self._session)
        if not len(events):
            return []

        seller_value = {}
        results = []

        def get_expenses_by_seller(evt: pastperfect.Event):
            nonlocal seller_value

            if evt.name != EXPENSE_MADE:
                return

            d = evt.data.get("description")
            if self._seller and self._seller not in d:
                return

            expense_date = datetime.strptime(evt.data.get("date_of"), "%Y-%m-%d")
            if self._since and expense_date < self._since:
                return

            if self._until and expense_date > self._until:
                return

            try:
                seller_value[d] = seller_value[d] + evt.data.get("value")
            except KeyError:
                seller_value[d] = evt.data.get("value")

        def get_expenses(evt: pastperfect.Event):
            nonlocal results
            if evt.name != EXPENSE_MADE:
                return

            d = evt.data.get("description")

            if self._seller and self._seller not in d:
                return

            expense_date = datetime.strptime(evt.data.get("date_of"), "%Y-%m-%d")
            if self._since and expense_date < self._since:
                return

            if self._until and expense_date > self._until:
                return

            results.append(
                [
                    evt.data.get("value"),
                    d,
                    evt.data.get("date_of"),
                ]
            )

        handler = get_expenses
        if self._group_seller:
            handler = get_expenses_by_seller

        events.replay([handler])

        if self._group_seller:
            results = [[value, key] for key, value in seller_value.items()]

        return results
