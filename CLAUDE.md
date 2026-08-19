# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**tracker-backend** is the REST API and web dashboard for tracker-app. It receives geofence events from Android devices and stores them in PostgreSQL.

- `POST /api/arrivals/` — record an arrival (requires `X-API-Key` header)
- `GET /api/arrivals/` — list history as JSON (unauthenticated)
- `GET /` — web dashboard with table + Leaflet map (unauthenticated)

## Stack

- Python 3.12 + Django 5.1 + Django REST Framework
- PostgreSQL 16
- Docker Compose: nginx (port 8001) → gunicorn (8000) + db
- `django-cors-headers` for CORS (configured via `CORS_ALLOW_ALL_ORIGINS` / `CORS_ALLOWED_ORIGINS` in `.env`)

## Commands

```bash
# Start all services
docker compose up -d --build

# Follow app logs
docker compose logs -f app

# Run migrations
docker compose exec app python manage.py migrate

# Create superuser
docker compose exec app python manage.py createsuperuser

# Django shell
docker compose exec app python manage.py shell

# Run all tests
docker compose exec app python manage.py test

# Run a single test
docker compose exec app python manage.py test apps.arrivals.tests.ArrivalAPITest.test_valid_arrival

# Django system checks
docker compose exec app python manage.py check
```

## Initial Setup

```bash
cp .env.example .env
# Edit .env with your values
docker compose up -d --build
```

## Structure

```
config/          ← settings, urls, wsgi
apps/arrivals/   ← Arrival model, serializer, views, urls
templates/       ← dashboard.html (Leaflet + table)
nginx/           ← nginx.conf
```

## Arrival Model

The `Arrival` model stores: `latitude`, `longitude`, `device_id`, `event_type`, and `timestamp`. Valid `event_type` values: `"enter"`, `"exit"`, `"stationary"` (stationary is sent by the Android app when the device has been motionless outside the zone for 10+ minutes).

## API Authentication

`POST /api/arrivals/` validates the `X-API-Key` header against `TRACKER_API_KEY` in `.env`. If `TRACKER_API_KEY` is empty, the endpoint is open (useful for development). `GET` endpoints and the dashboard are always unauthenticated.

## Settings Notes

- Locale: `es-ec`, timezone: `America/Guayaquil`
- `TRACKER_API_KEY` is read from `.env` via `python-decouple` and stored in `settings.TRACKER_API_KEY`
- All DB credentials come from `.env` (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`)
