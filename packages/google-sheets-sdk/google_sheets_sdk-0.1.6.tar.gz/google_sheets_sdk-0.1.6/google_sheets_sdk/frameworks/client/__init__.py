from dataclasses import InitVar, dataclass, field
from typing import ClassVar


from google_sheets_sdk.entities import spreadsheet as spreadsheet_entity
from google_sheets_sdk.entities import Settings, Sheet, Token

from httpx import AsyncClient, HTTPStatusError


@dataclass
class Client:
    _base_url: ClassVar[str] = "https://sheets.googleapis.com/"

    _http_client: "AsyncClient"
    _token: Token = field(
        init=False,
    )
    settings: InitVar[Settings]

    def __post_init__(
        self,
        settings: Settings,
    ):
        self._token = Token(
            email=settings.CLIENT_EMAIL,
            base_url=self._base_url,
            scope=settings.SCOPE.unicode_string(),
            private_key=settings.PRIVATE_KEY.replace(r"\n", "\n"),
            private_key_id=settings.PRIVATE_KEY_ID,
        )

    async def batch_clear_values(
        self,
        spreadsheet_id: spreadsheet_entity.Id,
        ranges: list[str],
    ) -> None:
        try:
            response = await self._http_client.post(
                url=f"{self._base_url}v4/spreadsheets/{spreadsheet_id}/values:batchClear",
                json={
                    "ranges": ranges,
                },
                headers={
                    "Authorization": f"Bearer {self._token.encoded}",
                },
            )
            response.raise_for_status()
        except HTTPStatusError as exc:
            raise exc

    async def batch_update_values(
        self,
        spreadsheet_id: spreadsheet_entity.Id,
        sheets: list[Sheet],
    ) -> spreadsheet_entity.BatchUpdateValuesResponse:
        try:
            response = await self._http_client.post(
                url=f"{self._base_url}v4/spreadsheets/{spreadsheet_id}/values:batchUpdate",
                json={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        sheet.model_dump(
                            mode="json",
                        )
                        for sheet in sheets
                    ],
                },
                headers={
                    "Authorization": f"Bearer {self._token.encoded}",
                },
            )
            response.raise_for_status()
        except HTTPStatusError as exc:
            raise exc
        else:
            return spreadsheet_entity.BatchUpdateValuesResponse(**response.json())
