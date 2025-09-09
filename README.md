# SMS Setup Guide

## Prerequisites

- Linux OS
- Python 3.11+
- Docker & Docker Compose
- Git


### 1. Install UV (Python Package Manager)

```bash
# Install UV using pip
pip install uv

# Or install using curl (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### 2. Clone and Setup Project

```bash
# Clone repository
git clone <repo-url>
cd <project-name>

# Sync dependencies from pyproject.toml
uv sync
```

## UV Package Management

### Basic Commands

```bash
# Add new dependency
uv add django
uv add requests
uv add "django>=4.2,<5.0"

# Add development dependency
uv add pytest --dev
uv add black --dev

# Remove dependency
uv remove django
uv remove pytest

# Update all dependencies
uv sync --upgrade

# Update specific package
uv add django --upgrade

# Install from requirements.txt (if migrating)
uv add -r requirements.txt
```

### Virtual Environment
 
UV automatically creates virtual environment and utilize it.
```bash
# run commands directly with UV
uv run python manage.py runserver
uv run python manage.py migrate
```

## Docker Setup

### 1. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

Fill in your `.env` file:

### 2. Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop and remove volumes
docker-compose down -v
```

## Common Commands

```bash
# Django management
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py collectstatic
uv run python manage.py shell
```