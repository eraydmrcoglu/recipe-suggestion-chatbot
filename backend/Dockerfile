FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install --no-cache-dir poetry==1.4.2 &&\
    poetry config virtualenvs.create false

RUN poetry install

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000"]
