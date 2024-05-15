from pydantic import BaseModel

type range = str
type value = str | int | float


class Sheet(BaseModel):
    range: range
    values: list[list[value]]
