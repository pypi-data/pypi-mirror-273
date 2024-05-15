from pydantic import BaseModel
from pydantic.fields import Field

type Id = str


class UpdateValuesResponse(BaseModel):
    spreadsheet_id: str = Field(
        ...,
        alias="spreadsheetId",
    )
    updated_range: str = Field(
        default=0,
        alias="updatedRange",
    )
    updated_rows: int = Field(
        default=0,
        alias="updatedRows",
    )
    updated_columns: int = Field(
        default=0,
        alias="updatedColumns",
    )
    updated_cells: int = Field(
        default=0,
        alias="updatedCells",
    )


class BatchUpdateValuesResponse(BaseModel):
    spreadsheet_id: str = Field(
        ...,
        alias="spreadsheetId",
    )
    total_updated_rows: int = Field(
        default=0,
        alias="totalUpdatedRows",
    )
    total_updated_columns: int = Field(
        default=0,
        alias="totalUpdatedColumns",
    )
    total_updated_cells: int = Field(
        default=0,
        alias="totalUpdatedCells",
    )
    total_updated_sheets: int = Field(
        ...,
        alias="totalUpdatedSheets",
    )
    responses: list[UpdateValuesResponse]
