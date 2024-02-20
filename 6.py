import asyncio
from enum import Enum
from typing import List
from datetime import timedelta
from dataclasses import dataclass


timeout_seconds = timedelta(seconds=15).total_seconds()


@dataclass
class Payload:
    data: str


@dataclass
class Address:
    address: str


@dataclass
class Event:
    recipients: List[Address]
    payload: Payload


class Result(Enum):
    Accepted = 1
    Rejected = 2


async def read_data() -> Event:
    payload = Payload(data="Hello, world!")
    recipient1 = Address(address="recipient1@example.com")
    recipient2 = Address(address="recipient2@example.com")
    return Event(recipients=[recipient1, recipient2], payload=payload)


async def send_data(dest: Address, payload: Payload) -> Result:
    print(f"Sending data '{payload.data}' to {dest.address}")
    return Result.Accepted


async def perform_operation() -> None:
    while True:
        try:
            event = await read_data()
            for recipient in event.recipients:
                result = await send_data(recipient, event.payload)
                if result == Result.Rejected:
                    print(f"Sending data to {recipient.address} failed. Retrying...")
                    await asyncio.sleep(5)
                    await send_data(recipient, event.payload)
            print("Data processing complete")
        except Exception as e:
            print(f"An error occurred: {e}")

asyncio.run(perform_operation())

