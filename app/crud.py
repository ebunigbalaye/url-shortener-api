"""The actual database operations: create_url(), get_url_by_slug(), increment_click_count(),delete_url(), list_urls(). 
This is the layer between routes and the database — routes call these functions, 
they don't write raw queries inline."""

from app.utils.slug_generator import *
from app.models import URL
from datetime import datetime, timedelta, UTC
from sqlalchemy import select
from sqlalchemy.orm import Session

def create_shortened_url_using_db_id(database_session:Session, original_url:str)->URL:
    id,slug = generate_base62_slug(database_session)
    created_at = datetime.now(UTC)
    url_db_object = URL(id = id,slug=slug, original_url=original_url, created_at=created_at, expires_at=created_at + timedelta(days=7))
    database_session.add(url_db_object)
    database_session.commit()
    return url_db_object
    


def create_shortened_url_using_hash(database_session:Session, original_url:str)->URL:
    slug = generate_sha256_slug(original_url)
    created_at = datetime.now(UTC)
    url_db_object = URL(slug=slug, original_url=original_url, created_at=created_at, expires_at=created_at + timedelta(days=7))
    database_session.add(url_db_object)
    database_session.commit()
    return url_db_object


def get_by_slug(database_session:Session, slug:str)-> URL:
    stmt = select(URL).where(URL.slug == slug)
    url_db_object = database_session.execute(stmt).scalar_one_or_none()
    return url_db_object

def increment_click_count(database_session:Session,url_db_object:URL):
    if url_db_object is None:
        raise ValueError("Object not Found")
    url_db_object.click_count += 1
    database_session.commit()
    

def delete_by_slug(database_session:Session,url_db_object:URL):
    if url_db_object is None:
        raise ValueError("Object not Found")
    database_session.delete(url_db_object)
    database_session.commit()


def list_urls(db: Session, cursor: int | None = None, limit: int = 20):
    query = select(URL).order_by(URL.id.asc())
    if cursor is not None:
        query = query.where(URL.id > cursor)
    query = query.limit(limit)
    urls = db.execute(query).scalars().all()
    if len(urls) == limit:
         next_cursor = urls[-1].id 
    else :
        next_cursor = None
    return urls, next_cursor