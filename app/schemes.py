from datetime import date

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator


class BookSchema(BaseModel):
    id: str
    author: str
    title: str
    pages_number: int
    date_start: date | None
    date_end: date | None
    comment: str | None
    rating: int | None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('id', mode='before')
    def cast_to_str(cls, value) -> str:
        return str(value)

    @field_serializer('date_start', 'date_end')
    def format_dates(dt, _info):
        if dt is None:
            return dt

        return dt.strftime('%Y-%m-%d')


class AddBookSchema(BaseModel):
    author: str
    title: str
    pages_number: int
    date_start: date | None = None
    date_end: date | None = None
    comment: str | None = None
    rating: int | None = None


class EditBookSchema(BaseModel):
    author: str | None = None
    title: str | None = None
    pages_number: int | None = None
    date_start: date | None = None
    date_end: date | None = None
    comment: str | None = None
    rating: int | None = None
