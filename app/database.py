"""Sets up the SQLAlchemy engine, session factory, and a get_db() dependency that FastAPI injects into routes.
 This is the only file that knows how the app connects to Postgres"""