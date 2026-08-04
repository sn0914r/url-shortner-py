from collections import Counter
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
    db: AsyncSession,
    short_code: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
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


async def get_url_stats(db: AsyncSession, short_code: str) -> dict:
    stmt = select(Url).where(Url.short_code == short_code)
    result = await db.execute(stmt)
    url_obj = result.scalar_one_or_none()

    if not url_obj:
        raise HTTPException(status_code=404, detail="Short URL not found")

    click_stmt = select(Click).where(Click.url_id == url_obj.id)
    click_result = await db.execute(click_stmt)
    clicks = click_result.scalars().all()

    stats = {
        "total_clicks": len(clicks),
        "browsers": dict(Counter([c.user_agent or "Unknown" for c in clicks])),
        "ips": dict(Counter([c.ip_address or "Unknown" for c in clicks])),
        "timeline": dict(Counter([c.clicked_at.strftime("%Y-%m-%d") for c in clicks])),
    }

    return stats
