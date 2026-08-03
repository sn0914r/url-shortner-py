from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.links import schemas, services

from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/link", tags=["Links"])


@router.post(
    "/", response_model=schemas.URLResponse, status_code=status.HTTP_201_CREATED
)
async def create_url(url_data: schemas.URLCreate, db: AsyncSession = Depends(get_db)):
    new_url = await services.create_short_url(db, str(url_data.long_url))
    return new_url


@router.get("/{short_code}")
async def redirect_to_url(
    short_code: str, request: Request, db: AsyncSession = Depends(get_db)
):
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    long_url = await services.get_long_url(
        db, short_code, ip_address=ip, user_agent=user_agent
    )
    return RedirectResponse(url=long_url)
