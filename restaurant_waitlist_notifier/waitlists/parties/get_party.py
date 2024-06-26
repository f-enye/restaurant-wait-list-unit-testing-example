from datetime import datetime

from httpx import get
from pydantic import BaseModel

from restaurant_waitlist_notifier.secrets.get_secret import get_secret


class Party(BaseModel):
    name: str
    phone_number: str
    size: int
    time_of_arrival: datetime
    quoted_time_in_minutes: int
    notes: str | None = None


def get_party(guid: str) -> Party:
    waitlist_api_key = get_secret("waitlist_api_key")
    result = get(
        f"https://waitlist.example.com/party/{guid}",
        headers={"X-API-KEY": waitlist_api_key},
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
