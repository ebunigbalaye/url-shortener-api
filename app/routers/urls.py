"""The route handlers themselves — this is where your endpoints live:
POST /shorten
GET /{slug} (redirect)
GET /stats/{slug}
DELETE /{slug}
GET /urls (paginated list)
Each handler validates input (via the Pydantic schema),
 calls the relevant crud.py function, and returns a response. No business logic here beyond orchestration."""