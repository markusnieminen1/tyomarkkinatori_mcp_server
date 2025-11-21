FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . /app

RUN uv sync --locked

RUN rm -rf \
    /app/tests \
    /app/data/ammatit.json \
    /app/.gitignore \
    /app/dockerfile \
    /app/LICENSE \
    /app/noutorajapintaohje.pdf \
    /app/README.md \
    /app/pyproject.toml \
    /app/uv.lock

RUN adduser --disabled-password --gecos "" --uid 1001 appuser \
    && chown -R appuser:appuser /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "mcp_server.main"]
