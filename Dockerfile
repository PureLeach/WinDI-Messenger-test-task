FROM python:3.11-slim AS builder

RUN pip install --upgrade pip pipenv

WORKDIR /tmp
COPY Pipfile Pipfile.lock ./

RUN pipenv requirements > requirements.txt

FROM python:3.11-slim AS final

RUN useradd -m appuser

WORKDIR /app

COPY --from=builder /tmp/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY project/ ./project/
COPY .env .env
COPY entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
