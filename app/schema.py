"""Pydantic models — the "shape" of data going in and out of the API (request bodies, response bodies).
 Kept separate from models.py on purpose: your DB schema and your API contract are allowed to differ 
 (e.g., you might hide id from responses, or require different fields on create vs. read)."""
import datetime
from typing import Optional
from pydantic import  BaseModel

class CreateSchema(BaseModel):
    original_url: str               

class ResponseSchema(BaseModel):
    id: int                      # Required field
    slug: str                # Required field
    original_url: str            # Required field
    created_at: datetime.datetime  # Required field

class StatsSchema(BaseModel):
    slug: str                # Required field
    click_count: int              # Required field
    created_at: datetime.datetime  # Required field
    expires_at: Optional[datetime.datetime] = None  # Optional field