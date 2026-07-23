FROM python:3.13
WORKDIR /usr/local/app


# Install the application dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv sync --frozen --no-dev

# Copy in the source code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd -m appuser
USER appuser

CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]