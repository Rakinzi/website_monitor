# Project Overview

This is a web health monitoring application with a Svelte frontend and a Python FastAPI backend.

## Frontend (`monitor_front/`)

The frontend is a modern website monitoring dashboard built with Svelte 5, Vite, and Skeleton UI.

### Building and Running (Frontend)

- **Install dependencies:** `bun install` or `npm install`
- **Run development server:** `bun run dev` or `npm run dev`
- **Build for production:** `bun run build` or `npm run build`
- **Type check:** `bun run check` or `npm run check`

### Development Conventions (Frontend)

- Code is written in TypeScript and Svelte.
- Styling is done with Tailwind CSS and Skeleton UI.
- Routing is handled by `svelte-spa-router`.
- API calls are managed in `src/lib/services/api.ts`.

## Backend (`webhealth-backend/`)

The backend is a FastAPI application that provides a REST API for the frontend.

### Building and Running (Backend)

- **Install dependencies:** `uv pip install -r requirements.txt` (assuming a `requirements.txt` is generated from `pyproject.toml`)
- **Run development server:** `uvicorn app.main:app --reload` from within the `src` directory.

### Development Conventions (Backend)

- The application is built with Python and FastAPI.
- It uses SQLAlchemy for asynchronous database operations.
- Authentication is handled with JWT.
- Background tasks are managed with a scheduler.
- Cybersecurity checks are a core feature, with a strict passive-only policy.
