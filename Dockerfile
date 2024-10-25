# Use the Python 3.10 base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# Set working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copy the Poetry files (pyproject.toml and poetry.lock) to the container
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the entire project into the container
COPY . .

# Run Django's development server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
