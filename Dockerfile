FROM python:3.10-alpine

WORKDIR /app
RUN apk add git

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY main.py /app
COPY ohdieux /app/ohdieux

ENV PYTHONPATH /app

RUN adduser app -G nobody -u 2000 -D -H
#RUN chown -R app:app /app
USER app:nobody

EXPOSE 8080
CMD ["gunicorn", "--workers=1", "--threads=8","--timeout=10","--bind=0.0.0.0:8080", "main"]