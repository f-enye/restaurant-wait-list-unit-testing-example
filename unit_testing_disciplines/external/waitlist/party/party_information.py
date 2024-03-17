from dataclasses import dataclass
from datetime import datetime

import requests


@dataclass(frozen=True)
class Party:
    name: str
    phone_number: str
    size: int
    time_of_arrival: datetime
    quoted_time_in_minutes: int
    notes: str | None = None


def get_party(bearer_token: str, guid: str) -> Party:
    result = requests.get(
        "https://waitlist.example.com/party/{guid}",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )
    result.raise_for_status()
    response = result.json()
    return Party(
        name=response["name"],
        phone_number=response["phone_number"],
        time_of_arrival=response["time_of_arrival"],
        quoted_time_in_minutes=response["quoted_time_in_minutes"],
    )
