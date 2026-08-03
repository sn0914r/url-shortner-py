from app.modules.links.models import Click
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: I001
from app.modules.links.models import Url
from app.modules.links.utils import generate_short_code
from fastapi import HTTPException
from sqlalchemy import select


async def create_short_url(db: AsyncSession, long_url: str) -> Url:
    code = generate_short_code()

    new_url = Url(long_url=long_url, short_code=code)

    db.add(new_url)
    await db.commit()

    await db.refresh(new_url)

    return new_url


async def get_long_url(
    db: AsyncSession, short_code: str, ip_address: str | None = None, user_agent: str | None = None
) -> str:
    stmt = select(Url).where(Url.short_code == short_code)
    result = await db.execute(stmt)
    url_obj = result.scalar_one_or_none()

    if not url_obj:
        raise HTTPException(status_code=404, detail="Short URL not found")

    new_click = Click(url_id=url_obj.id, ip_address=ip_address, user_agent=user_agent)
    db.add(new_click)
    await db.commit()

    return url_obj.long_url
