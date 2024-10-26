# SkyLock - API

This is a FastAPI-based application for managing file sharing with features like user registration, authentication, and more.

## Requirements

Before starting, make sure you have the following installed:

- Python 3.12+
- Docker & Docker Compose (optional, if you prefer to run with Docker)

## Getting Started

### Configuration

Before running the application, you need to create a `.env` file in the root directory of your project with the following environment variables:

```dotenv
# .env file
JWT_SECRET=<your-jwt-secret>
DATABASE_URL=<your-database-url>
```

Make sure to replace the `JWT_SECRET` with your own secure secret key and configure `DATABASE_URL` according to your database setup.

## How to run

### Option 1: Running with Docker Compose

**Build and start the containers**:

```bash
docker-compose up --build
```

### Option 2: Running with Poetry

**1. Enter Poetry virtual environment:**

```bash
poetry shell
```

**2. Install dependencies:**

```bash
poetry install
```

**3. Start the application using entry point:**

```bash
./entrypoint_dev.sh
```

## Database Migration

When you make changes to your database schema, you need to perform a migration. Here's how to do it:

1. **Generate a New Migration**: Whenever you modify your SQLAlchemy models, generate a new migration file using Alembic:

   ```bash
   alembic revision --autogenerate -m "description_of_changes"
   ```

2. **Apply the Migration**: After generating the migration file, apply the changes to your database (entrypoint does that for you as well):

   ```bash
   alembic upgrade head
   ```

3. **Review Migration Scripts**: It's a good practice to review the generated migration scripts before applying them to ensure they reflect the intended changes.

## API documentation

After running the app, the full API documentation will be available at:

- **Swagger UI:** <http://localhost:8000/docs>
- **Redoc:** <http://localhost:8000/redoc>
