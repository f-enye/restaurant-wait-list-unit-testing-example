from enum import Enum

from unit_testing_disciplines.external.waitlist.party.get_party import Party


class Notifications(Enum):
    added_to_waitlist = "added_to_waitlist"
    table_prepared = "table_prepared"
    waitlist_delayed = "waitlist_delayed"


def get_message(party: Party, notification: str) -> str:
    return _strategies[Notifications(notification)](party)


def _get_added_to_waitlist_message(party: Party) -> str:
    return f"Welcome, we've added you to our waitlist. We expect to have your table prepared in about {party.quoted_time_in_minutes} minutes."


def _get_table_prepared_message(party: Party) -> str:
    return "Hello, you're table is ready. To get seated please see the host."


def _get_waitlist_delayed_message(party: Party) -> str:
    return "Apologies, it is taking longer than expected to finish preparing your table. Please see the host if you have any questions."


_strategies = {
    Notifications.added_to_waitlist: _get_added_to_waitlist_message,
    Notifications.table_prepared: _get_table_prepared_message,
    Notifications.waitlist_delayed: _get_waitlist_delayed_message,
}
