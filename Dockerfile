FROM python:3.12-slim

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

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install 

COPY /ticket_booking .

EXPOSE 8000

ENTRYPOINT [ "poetry","run","python", "manage.py"]

CMD [ "runserver", "0.0.0.0:8000"]
