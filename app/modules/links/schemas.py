from pydantic import BaseModel, HttpUrl  # noqa: I001
from datetime import datetime


class URLCreate(BaseModel):
    long_url: HttpUrl


class URLResponse(BaseModel):
    id: int
    short_code: str
    long_url: str
    created_at: datetime

    class Config:
        from_attributes = True


class ClickStats(BaseModel):
    total_clicks: int
    browsers: dict[str, int]
    ips: dict[str, int]
    timeline: dict[str, int]
