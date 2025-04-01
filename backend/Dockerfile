FROM python:3.13

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY . .

EXPOSE 8000
