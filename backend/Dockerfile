# Python 3.11 Slim Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set env variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy application code
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini

# Create non-root user for security
# RUN useradd -m myuser
# USER myuser

# Expose port (Render/Heroku/Railway usually assign a PORT env var, but we document 8000)
EXPOSE 8000

# Command to run the application
# We use a shell script or direct command. 
# For prod, we often want to run migrations first, then start app.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
