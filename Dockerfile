FROM python:3.12-alpine as pipenv
WORKDIR /app
RUN pip install pipenv
COPY Pipfile.lock .
COPY Pipfile .
RUN pipenv requirements > requirements.txt


FROM python:3.12-alpine
WORKDIR /app
RUN apk add git
COPY --from=pipenv /app/requirements.txt .
RUN pip install -r requirements.txt

COPY main.py /app
COPY main_worker.py /app
COPY ohdieux /app/ohdieux

ENV PYTHONPATH /app

USER 2000:2000

EXPOSE 8080
CMD ["sh", "-c", "gunicorn --workers=${GUNICORN_WORKERS:-1} --threads=${GUNICORN_THREADS:-4} --timeout=10 --bind=0.0.0.0:${PORT:-8080} main"]
