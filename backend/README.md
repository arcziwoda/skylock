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

## API documentation

After running the app, the full API documentation will be available at:

- **Swagger UI:** <http://localhost:8000/docs>
- **Redoc:** <http://localhost:8000/redoc>
