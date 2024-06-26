FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./

RUN apt-get update \
    && apt-get install -y default-jdk \
    && pip install --no-cache-dir -r /app/requirements.txt

ENV JAVA_HOME=/usr/lib/jvm/default-java

COPY ./ ./

CMD ["python", "manage.py","runserver","0.0.0.0:8000"]