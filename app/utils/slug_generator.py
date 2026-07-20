"""Isolated slug-generation logic — this is where you'll experiment with your two approaches from
 the roadmap (base62-encoded counter vs. truncated MD5 hash).
Keeping it separate means you can swap strategies without touching routes or CRUD code."""
import hashlib
import secrets
from sqlalchemy import Sequence
from app.database import SessionLocal
import pybase62



# functions for generating a truncated hash for the slug
def generate_salt():
    # Generate a 16-byte salt for password hashing
    salt = secrets.token_bytes(16)
    return salt
def generate_sha256_slug(original_url: str) -> str:
    slug_length = 5
    # Convert string to bytes and feed it to sha256
    encoded_data = original_url.encode('utf-8')
    salt = generate_salt()
    hash = hashlib.sha256(encoded_data+salt)
    # Return the 64-character hexadecimal representation
    return hash.hexdigest()[:slug_length]

#function to generate slug by converting the database id to base 62
def generate_base62_slug():
    with SessionLocal() as session:
        next_id = session.execute(Sequence("urls_id_seq")).scalar()
         # 1. Encoding the database ID
        slug = pybase62.encode(next_id)
        return slug



