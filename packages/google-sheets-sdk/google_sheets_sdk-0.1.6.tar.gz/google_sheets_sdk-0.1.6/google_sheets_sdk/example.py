import asyncio

import httpx

from google_sheets_sdk import Client
from google_sheets_sdk.entities import Settings, Sheet


async def main():
    async with httpx.AsyncClient() as _client:
        client = Client(
            _client,
            settings=Settings(),  # type: ignore
        )


if __name__ == "__main__":
    asyncio.run(main())
