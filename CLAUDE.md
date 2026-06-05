# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**tracker-backend** es la API REST y dashboard web para tracker-app. Recibe eventos de llegada a geocercas desde dispositivos Android y los almacena en PostgreSQL.

- `POST /api/arrivals/` — registra una llegada (requiere header `X-API-Key`)
- `GET /api/arrivals/` — lista el historial en JSON
- `GET /` — dashboard web con tabla + mapa Leaflet

## Stack

- Python 3.12 + Django 5.1 + Django REST Framework
- PostgreSQL 16
- Docker Compose: nginx (8001) → gunicorn (8000) + db

## Comandos

```bash
# Levantar todos los servicios
docker compose up -d

# Ver logs
docker compose logs -f app

# Crear superusuario
docker compose exec app python manage.py createsuperuser

# Migraciones
docker compose exec app python manage.py makemigrations
docker compose exec app python manage.py migrate

# Shell Django
docker compose exec app python manage.py shell
```

## Setup inicial

```bash
cp .env.example .env
# Editar .env con tus valores
docker compose up -d --build
```

## Estructura

```
config/          ← settings, urls, wsgi
apps/arrivals/   ← modelo Arrival, serializer, views, urls
templates/       ← dashboard.html (Leaflet + tabla)
nginx/           ← nginx.conf
```

## Autenticación de la API

El endpoint `POST /api/arrivals/` valida el header `X-API-Key` contra `TRACKER_API_KEY` en `.env`. Si `TRACKER_API_KEY` está vacío, el endpoint queda abierto (útil en desarrollo).
