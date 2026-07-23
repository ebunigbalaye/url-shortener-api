"""The route handlers themselves — this is where your endpoints live:Each handler validates input (via the Pydantic schema),the relevant crud.py function, and returns a response.."""

from fastapi import APIRouter,Depends,Query,HTTPException,status
from fastapi.responses import RedirectResponse
from app.schema import *
from app.crud import *
from app.database import get_session

router = APIRouter()


@router.post("/shorten",status_code=201,response_model=URLResponseSchema)
def shorten_url(request: CreateSchema,db: Session = Depends(get_session)):
    return create_shortened_url_using_db_id(db, request.original_url)

@router.post("/shortenhash",status_code=201,response_model=URLResponseSchema)
def shorten_url(request: CreateSchema,db: Session = Depends(get_session)):
    return create_shortened_url_using_hash(db, request.original_url)

@router.get("/urls", response_model=PaginatedURLResponse)
def get_urls(cursor: int | None = None, limit: int = Query(default=20, le=100),db: Session = Depends(get_session)):
    rows, next_cursor = list_urls(db, cursor=cursor, limit=limit)
    return {  "items": rows,    "next_cursor": next_cursor}

@router.get("/stats/{slug}",response_model=URLStatsSchema)
def get_stats(slug:str, db: Session=Depends(get_session)):
    url = get_by_slug(db,slug) 
    return url

@router.get("/{slug}")
def redirect(slug:str, db: Session=Depends(get_session)):
    url = get_by_slug(db,slug)
    if url is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Site not found")
    increment_click_count(db,url)
    return RedirectResponse(url.original_url,status_code=302)


@router.delete("/delete/{slug}", status_code=204)
def delete_slug(slug: str, db: Session = Depends(get_session)):
    url = get_by_slug(db, slug)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    delete_by_slug(db, url)
    