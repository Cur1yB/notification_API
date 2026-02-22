# Notifications service

FastAPI + Tortoise ORM + Postgres.
JWT authentication.
CRUD operations for notifications available only for current user.

## Deploy link

[Render](https://notification-api-0ggu.onrender.com/)

## Run

Rename `.env.example` to `.env` and fill required environment variables.

Run developer service
```bash
make run
```

Docs: http://localhost:8000/docs

## Requests (curl)

Register:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"pupalupa","password":"lupapupa"}'
```

Login:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"pupalupa","password":"lupapupa"}'
```

Create notification:
```bash
curl -X POST http://localhost:8000/notifications/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <ACCESS>' \
  -d '{"type":"like","text":"Hello"}'
```

List notifications:
```bash
curl 'http://localhost:8000/notifications/?limit=20&offset=0' \
  -H 'Authorization: Bearer <ACCESS>'
```

Delete notification:
```bash
curl -X DELETE http://localhost:8000/notifications/1 \
  -H 'Authorization: Bearer <ACCESS>'
```
## Tests

The project includes unit and integration tests.

Tests can be run using:

```bash
make pytest
```

Script `scripts/run_tests.sh` uses Docker Compose to spin up the test environment and executes the integration tests using `pytest`.

---

================================== tests coverage ==================================
```bash
Name                                            Stmts   Miss  Cover
-------------------------------------------------------------------
...
-------------------------------------------------------------------
TOTAL                                             542      9    98%
```

================================== project structure ==================================

```bash
app
├── db_services
│   ├── __init__.py
│   ├── notifications.py
│   └── users.py
├── dependencies
│   ├── __init__.py
│   └── auth.py
├── models
│   ├── __init__.py
│   ├── enums.py
│   ├── notifications.py
│   └── users.py
├── routers
│   ├── auth.py
│   └── notifications.py
├── schemas # rest models
│   ├── __init__.py
│   ├── auth.py
│   └── notifications.py
├── services
│   ├── __init__.py
│   ├── auth.py
│   └── notifications.py
├── db.py
├── exceptions.py
├── handlers.py
├── main.py
├── security.py
└── settings.py
tests
├── integration
│   ├── __init__.py
│   ├── test_auth_routes.py
│   └── test_notification_routes.py
├── unit
│   ├── __init__.py
│   ├── dummies.py
│   ├── test_auth_services.py
│   └── test_notifications_services.py
├── __init__.py
└── conftest.py
scripts
└── run_tests.sh
Dockerfile
docker-compose.test.yml
docker-compose.yaml
Makefile
README.md
package-lock.json
package.json
pyproject.toml
uv.lock
```