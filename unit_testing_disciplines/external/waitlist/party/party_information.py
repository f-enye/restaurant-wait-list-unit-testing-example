from datetime import datetime

from httpx import get
from pydantic import BaseModel


class Party(BaseModel):
    name: str
    phone_number: str
    size: int
    time_of_arrival: datetime
    quoted_time_in_minutes: int
    notes: str | None = None


def get_party(bearer_token: str, guid: str) -> Party:
    result = get(
        "https://waitlist.example.com/party/{guid}",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )
    result.raise_for_status()
    response = result.json()
    return Party(
        name=response["name"],
        phone_number=response["phone_number"],
        time_of_arrival=response["time_of_arrival"],
        size=response["size"],
        quoted_time_in_minutes=response["quoted_time_in_minutes"],
    )
