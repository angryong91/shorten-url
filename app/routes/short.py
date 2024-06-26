from typing import List

from app.db.mysql import db
from app.exceptions import Conflict, NotFound
from app.models.short import ShortCreate, ShortInfo, ShortCounts, ShortId
from app.services.short import create_short, get_short, get_cache_url, set_cache_url, create_short_click, \
    count_short_click
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/short-links", status_code=201, response_model=ShortInfo)
def create_short_link(payload: ShortCreate, session: Session = Depends(db.get_db)):
    short = create_short(payload.url, session)
    if not short:
        raise Conflict()
    return ShortInfo(short_id=short.id, url=short.origin_url, created_at=short.created_at)


@router.get("/short-links/{short_id}", response_model=ShortInfo)
def get_original_url(short_id: str, session: Session = Depends(db.get_db)):
    short_id = ShortId(short_id=short_id).short_id
    short = get_short(ShortId(short_id=short_id).short_id, session)
    if not short:
        raise NotFound()
    return ShortInfo(short_id=short.id, url=short.origin_url, created_at=short.created_at)


@router.get("/r/{short_id}", response_class=RedirectResponse)
async def redirect_to_original(short_id: str, session: Session = Depends(db.get_db)):
    short_id = ShortId(short_id=short_id).short_id
    origin_url = get_cache_url(short_id)
    if not origin_url:
        short = get_short(short_id, session)
        if not short:
            raise NotFound()
        set_cache_url(short_id, short.origin_url)
        origin_url = short.origin_url

    await create_short_click(short_id)
    return RedirectResponse(origin_url, status_code=302)


@router.get("/count/{short_id}", status_code=200, response_model=List[ShortCounts])
async def count_shorts(short_id: str, session: Session = Depends(db.get_db)):
    short_id = ShortId(short_id=short_id).short_id
    short = get_short(short_id, session)
    if not short:
        raise NotFound()

    result = await count_short_click(short_id)
    return result
