# Email API

REST API for asynchronous sending of e-mail messages:
- to any recipient address,
- with body and subject defined in a template (`Template`),
- from a predefined, active sender mailbox (`Mailbox`).

## Technologies

Python 3.13, Django 6, Django REST Framework, PostgreSQL, Celery + RabbitMQ,
django-environ, django-filter, drf-spectacular (Swagger).

## Requirements

- [Docker](https://www.docker.com/) + Docker Compose
- [Poetry](https://python-poetry.org/) (for local runs)

## Environment configuration

Configuration is read from a `.env` file (via `django-environ`). Example:

```env
SECRET_KEY=django-insecure-change-me
DEBUG=True
DATABASE_URL=postgres://postgres:postgres@localhost:5432/email_api
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
```

## Running

### Option A — local (infrastructure in Docker)

1. Start the database and broker:

   ```bash
   docker compose up -d db rabbitmq
   ```

2. Install dependencies:

   ```bash
   poetry install --no-root
   ```

3. Run migrations and create an admin account:

   ```bash
   poetry run python manage.py migrate
   poetry run python manage.py createsuperuser
   ```

4. Start the server (terminal 1) and the Celery worker (terminal 2):

   ```bash
   poetry run python manage.py runserver
   poetry run celery -A core worker -l info
   ```

   > **Windows:** the default `prefork` pool does not work on Windows (no `fork()`).
   > Run the worker with the `solo` pool (or `threads`):
   >
   > ```bash
   > poetry run celery -A core worker -l info --pool=solo
   > ```

### Option B — everything in Docker

```bash
docker compose up --build
```

Starts the database, RabbitMQ, the Django server (with automatic migrations) and the Celery worker.

## Endpoints

| Method            | URL                      | Description                   |
|-------------------|--------------------------|-------------------------------|
| GET / POST        | `/api/mailboxes/`        | List / create mailboxes       |
| GET/PUT/PATCH/DEL | `/api/mailboxes/{id}/`   | Mailbox details / update      |
| GET / POST        | `/api/messages/`         | List / send messages          |
| GET/PUT/PATCH/DEL | `/api/messages/{id}/`    | Message details               |

Creating a message (`POST /api/messages/`) automatically schedules asynchronous
delivery via Celery (up to 3 retries on failure). Sending is only possible from an
active mailbox (`is_active=True`).

### Example — create a mailbox

```bash
curl -X POST http://127.0.0.1:8000/api/mailboxes/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sender",
    "email": "sender@example.com",
    "is_active": true,
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "smtp_username": "user",
    "smtp_password": "secret"
  }'
```

### Example — send a message

```bash
curl -X POST http://127.0.0.1:8000/api/messages/ \
  -H "Content-Type: application/json" \
  -d '{
    "mailbox": 1,
    "template_name": "welcome.html",
    "subject": "Welcome!",
    "receiver": "recipient@example.com"
  }'
```

## Filtering messages

| Parameter        | Example                                   | Description                            |
|------------------|-------------------------------------------|----------------------------------------|
| `is_sent`        | `/api/messages/?is_sent=true`             | Sent status (`sent_at` is set)         |
| `created_after`  | `/api/messages/?created_after=2026-01-01` | Created after the given date           |
| `created_before` | `/api/messages/?created_before=2026-12-31`| Created before the given date          |

## API documentation (Swagger)

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Message templates

HTML files in the `templates/emails/` directory (e.g. `welcome.html`, `notification.html`).
The file name is passed in the `template_name` field when creating a message.

## Logging

Errors and delivery confirmations are written to `logs/email.log`.

## Git workflow

The project is developed following GitHub Flow (the `main` branch + short-lived feature branches, integrated via Pull Requests).