from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Party:
    name: str
    phone_number: str
    size: int
    time_of_arrival: datetime
    quoted_time_in_minutes: int
    notes: str | None = None


def getPartyInformation(guid: str):
    return Party(name="Peter", phone_number="5555555551", size=1, time_of_arrival=datetime(2024, 1, 1, 1, 0), quoted_time_in_minutes=30)