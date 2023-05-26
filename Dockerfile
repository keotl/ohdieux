FROM python:3.10-alpine

WORKDIR /app
RUN apk add git
COPY ohdieux /app/ohdieux
COPY requirements.txt /app
COPY main.py /app

RUN pip3 install -r requirements.txt

ENV PYTHONPATH /app

RUN adduser app -G nobody -u 2000 -D -H
#RUN chown -R app:app /app
USER app:nobody

EXPOSE 8080
CMD ["gunicorn", "--workers=1", "--threads=16","--timeout=10","--bind=0.0.0.0:8080", "main"]