from pydantic import BaseModel, HttpUrl  # noqa: I001
from datetime import datetime


class URLCreate(BaseModel):
    long_url: HttpUrl
    expires_at: datetime | None = None


class URLResponse(BaseModel):
    id: int
    short_code: str
    short_url: str
    long_url: str
    created_at: datetime
    expires_at: datetime | None = None

    class Config:
        from_attributes = True


class ClickStats(BaseModel):
    total_clicks: int
    browsers: dict[str, int]
    ips: dict[str, int]
    timeline: dict[str, int]
