from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.exceptions import Conflict, NotFound
from app.models.short import ShortCreate, ShortInfo
from app.services.short import create_short, get_short, get_cache_url, update_short_click, set_cache_url

router = APIRouter()


@router.post("/short-links", status_code=201, response_model=ShortInfo)
def create_short_link(payload: ShortCreate):
    short = create_short(payload.url)
    if not short:
        raise Conflict()
    return ShortInfo(short_id=short.id, url=short.origin_url, created_at=short.created_at)


@router.get("/short-links/{short_id}", response_model=ShortInfo)
def get_original_url(short_id: str):
    short = get_short(short_id)
    if not short:
        raise NotFound()
    return ShortInfo(short_id=short.id, url=short.origin_url, created_at=short.created_at)


@router.get("/r/{short_id}", response_class=RedirectResponse)
def redirect_to_original(short_id: str):
    origin_url = get_cache_url(short_id)
    if not origin_url:
        short = get_short(short_id)
        if not short:
            raise NotFound()
        set_cache_url(short_id, short.origin_url)
        origin_url = short.origin_url

    update_short_click(short_id)
    return RedirectResponse(origin_url, status_code=302)
