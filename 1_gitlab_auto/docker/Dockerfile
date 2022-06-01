FROM python:3.9.13-slim
COPY . /app
WORKDIR /app
RUN adduser --disabled-password --no-create-home execuser \
    && pip install -r requirements.txt \
    && mkdir /data \
    && chown execuser:execuser /data
USER execuser
ENTRYPOINT python3.9 main.py