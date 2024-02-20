import asyncio
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

timeout_seconds = timedelta(seconds=15).total_seconds()

class Response(Enum):
    Success = 1
    RetryAfter = 2
    Failure = 3

class ApplicationStatusResponse(Enum):
    Success = 1
    Failure = 2

@dataclass
class ApplicationResponse:
    application_id: str
    status: ApplicationStatusResponse
    description: str
    last_request_time: datetime
    retriesCount: Optional[int]

async def get_application_status1(identifier: str) -> Response:
    await asyncio.sleep(3)
    return Response.Success

async def get_application_status2(identifier: str) -> Response:
    await asyncio.sleep(3)
    return Response.RetryAfter

async def perform_operation(identifier: str) -> ApplicationResponse:
    start_time = datetime.now()
    
    tasks = [get_application_status1(identifier), get_application_status2(identifier)]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    success_responses = []
    retry_responses = []
    for response in responses:
        if isinstance(response, Response):
            if response == Response.Success:
                success_responses.append(response)
            elif response == Response.RetryAfter:
                retry_responses.append(response)
    
    if success_responses:
        return ApplicationResponse(
            application_id=identifier,
            status=ApplicationStatusResponse.Success,
            description="Success",
            last_request_time=datetime.now(),
            retriesCount=None
        )
    elif retry_responses:
        return ApplicationResponse(
            application_id=identifier,
            status=ApplicationStatusResponse.Failure,
            description="Retry after timeout",
            last_request_time=start_time,
            retriesCount=len(retry_responses)
        )
    else:
        return ApplicationResponse(
            application_id=identifier,
            status=ApplicationStatusResponse.Failure,
            description="All requests failed",
            last_request_time=start_time,
            retriesCount=None
        )

async def main():
    identifier = "example_id"
    result = await perform_operation(identifier)
    print(result)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

