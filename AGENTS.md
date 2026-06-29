# AGENTS.md - AI Assistant Configuration

## Project Overview

This is the **Full Stack FastAPI Template** - a production-ready full-stack application template featuring:

- **Backend**: FastAPI (Python) with SQLModel, PostgreSQL, Pydantic
- **Frontend**: React 19 with TypeScript, Vite, TanStack Query/Router, Tailwind CSS, shadcn/ui
- **Infrastructure**: Docker Compose, Traefik reverse proxy
- **Testing**: Pytest (backend), Playwright (frontend E2E)
- **Package Management**: uv (Python), Bun (Node.js)

## Key Directories

```
/workspace
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core configuration
│   │   ├── alembic/     # Database migrations
│   │   └── email-templates/
│   ├── tests/           # Backend tests
│   └── pyproject.toml   # Python dependencies
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── client/      # Generated API client
│   │   ├── components/  # UI components
│   │   ├── hooks/       # Custom React hooks
│   │   └── routes/      # Application routes
│   └── package.json     # Node.js dependencies
├── scripts/             # Utility scripts
├── .env                 # Environment configuration
├── compose.yml          # Docker Compose configuration
└── development.md       # Development guide
```

## Development Commands

### Backend (Python)

```bash
cd backend

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run development server
fastapi dev app/main.py

# Run tests
bash ./scripts/test.sh

# Run linter
uv run prek run --all-files

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend (TypeScript/React)

```bash
cd frontend

# Install dependencies
bun install

# Run development server
bun run dev

# Build for production
bun run build

# Run linting
bun run lint

# Generate API client from OpenAPI schema
bun run generate-client

# Run E2E tests
bunx playwright test
```

### Docker Compose

```bash
# Start full stack (development)
docker compose watch

# View logs
docker compose logs

# Stop services
docker compose stop [service_name]

# Run backend tests in container
docker compose exec backend bash scripts/tests-start.sh
```

## URLs (Local Development)

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Adminer (DB)**: http://localhost:8080
- **Traefik UI**: http://localhost:8090
- **MailCatcher**: http://localhost:1080

## Code Style & Quality

### Backend (Python)
- **Linter**: ruff
- **Formatter**: ruff-format
- **Type Checker**: mypy (strict mode)
- **Test Framework**: pytest
- **Coverage**: coverage.py

Configuration in `backend/pyproject.toml`:
- Python version: 3.14+
- Excludes: `venv`, `.venv`, `alembic`
- No print statements allowed in production code

### Frontend (TypeScript)
- **Linter/Formatters**: Biome
- **Type Checker**: TypeScript (strict)
- **Test Framework**: Playwright

Configuration in `frontend/package.json` and `biome.json`

## Important Guidelines

### Making Changes

1. **Backend Changes**:
   - Modify models in `backend/app/models.py`
   - Add API endpoints in `backend/app/api/`
   - Update CRUD operations in `backend/app/crud.py`
   - After API changes, regenerate frontend client: `bash ./scripts/generate-client.sh`

2. **Frontend Changes**:
   - Components in `frontend/src/components/`
   - Routes/pages in `frontend/src/routes/`
   - Custom hooks in `frontend/src/hooks/`

3. **Database Changes**:
   - Always create Alembic migrations for model changes
   - Test migrations locally before committing

### Testing Requirements

- All tests must pass before committing
- Update tests when changing functionality
- Backend tests: `bash ./scripts/test.sh`
- Frontend E2E: requires running Docker Compose stack first

### Pre-commit Hooks

The project uses `prek` (modern pre-commit alternative):
- Automatically runs on git commit
- Includes: ruff, mypy, biome, yaml/yml checks, whitespace trimming
- Install: `cd backend && uv run prek install -f`

## Environment Variables

Key variables in `.env`:
- `SECRET_KEY` - Security key (must be changed in production)
- `POSTGRES_PASSWORD` - Database password (must be changed in production)
- `FIRST_SUPERUSER` / `FIRST_SUPERUSER_PASSWORD` - Admin credentials
- `DOMAIN` - Base domain (default: localhost)
- `FRONTEND_HOST` - Frontend URL for email links
- `ENVIRONMENT` - local/staging/production

⚠️ **Never commit sensitive values** - use placeholder values like `changethis`

## Architecture Notes

### Backend
- Uses SQLModel (SQLAlchemy + Pydantic) for ORM
- JWT authentication
- Email support with Mailcatcher for local dev
- Sentry integration for error tracking
- CORS configured for frontend origins

### Frontend
- Uses generated OpenAPI client (`frontend/src/client/`)
- State management with TanStack Query
- Routing with TanStack Router
- UI components from shadcn/ui + Radix UI
- Dark mode support via next-themes

### Communication
- Backend exposes OpenAPI schema at `/api/v1/openapi.json`
- Frontend client auto-generated from OpenAPI schema
- Use `bash ./scripts/generate-client.sh` after backend API changes

## Common Workflows

### Adding a New Feature

1. **Backend**:
   - Add/modify models in `models.py`
   - Create Alembic migration
   - Add API endpoints
   - Add/update tests
   - Run `bash ./scripts/generate-client.sh`

2. **Frontend**:
   - Pull updated API client
   - Create components/hooks as needed
   - Add route if needed
   - Write/update E2E tests

### Debugging

- **Backend**: Use VS Code debugger (pre-configured) or `docker compose exec backend bash`
- **Frontend**: Local dev server with hot reload, or debug in Docker
- **Database**: Access via Adminer at http://localhost:8080
- **Emails**: View in MailCatcher at http://localhost:1080

## Contributing Guidelines

- For major changes, open a GitHub Discussion first
- Keep PRs focused on single changes
- All automated/AI-assisted code must have meaningful human review
- Don't submit PRs where automation effort < review effort
- Reference related issues in PR descriptions

## Troubleshooting

### Backend won't start
- Check database is running: `docker compose ps`
- Verify `.env` configuration
- Check logs: `docker compose logs backend`

### Frontend build fails
- Clear node_modules: `rm -rf node_modules && bun install`
- Regenerate API client
- Check TypeScript errors: `bun run lint`

### Tests failing
- Ensure Docker Compose stack is running for E2E tests
- Clean test data: `docker compose down -v`
- Check backend virtual environment is activated
