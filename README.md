# Shikaku Solver

## Descripción
Proyecto web para resolver Shikaku usando Angular + FastAPI + Docker.

## Arquitectura
- Frontend Angular servido con Nginx.
- Backend FastAPI usando solver.py.
- Docker Compose levanta ambos servicios en una arquitectura full-stack multicontenedor.

## Requisitos
- Docker
- Docker Compose

## Ejecución local
```bash
cp .env.example .env
docker compose up -d --build
```

## Acceso
http://localhost:8080

## Endpoints principales
- GET `/api/health`
- GET `/api/boards`
- POST `/api/solve`
- POST `/api/steps`
- POST `/api/solve-all`

## Apagar
```bash
docker compose down
```

## Ver logs
```bash
docker compose logs -f
```
