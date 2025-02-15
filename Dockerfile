FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    build-essential \
    python3-venv \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.in-project true

COPY poetry.lock pyproject.toml ./

RUN poetry install

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app .

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONPATH="/app"

COPY /ticket_booking .

EXPOSE 8000

ENTRYPOINT [ "python", "manage.py"]

CMD [ "runserver", "0.0.0.0:8000"]


