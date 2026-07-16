"""Pydantic models — the "shape" of data going in and out of the API (request bodies, response bodies).
 Kept separate from models.py on purpose: your DB schema and your API contract are allowed to differ 
 (e.g., you might hide id from responses, or require different fields on create vs. read)."""