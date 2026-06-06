## Requirements

- **Docker installed and running** on the host.
- The user running resmon-api must be in the `docker` group (sudoless Docker).

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # set API_TOKEN, optional CORS_ORIGINS (use * for all)
uvicorn main:app
```

## Simple auth

All endpoints require an `Authorization` header with the token from `.env`.
(The Swagger "Authorize" box doesn't work)

## Endpoints

```bash
curl -H "Authorization: APITOKEN" "http://localhost:8000/api/docker/containers/?targetStatus=running"
curl -H "Authorization: APITOKEN" "http://localhost:8000/api/docker/networks/"
curl -H "Authorization: APITOKEN" "http://localhost:8000/api/docker/volumes/"
curl -H "Authorization: APITOKEN" "http://localhost:8000/api/sys/cpucores/"
curl -H "Authorization: APITOKEN" "http://localhost:8000/api/sys/cpuload/?perCore=true"
curl -H "Authorization: APITOKEN" "http://localhost:8000/api/sys/ramutilization/"
curl -H "Authorization: APITOKEN" "http://localhost:8000/api/sys/diskusage/?path=/"
```
`targetStatus`: created, running, paused, restarting, exited, dead.

## Future work

- Logging
- More monitors
