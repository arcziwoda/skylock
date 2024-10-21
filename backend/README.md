# File Sharing API

This is a FastAPI-based application for managing file sharing with features like user registration, authentication, and more.

## Requirements

Before starting, make sure you have the following installed:

- Python 3.12+
- Docker & Docker Compose (optional, if you prefer to run with Docker)

## Getting Started

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

**3. Start the application:**

```bash
python -m zprp_file_sharing.main
```

## API documentation

After running the app, the full API documentation will be available at:

- **Swagger UI:** '<http://localhost:8000/docs>'
- **Redoc:** '<http://localhost:8000/redoc>'
