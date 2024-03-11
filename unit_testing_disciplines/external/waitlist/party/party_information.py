from dataclasses import dataclass


@dataclass(frozen=True)
class Party:
    name: str
    phone_number: str


def getPartyInformation(guid: str):
    return Party(name="Peter", phone_number="5555555551")