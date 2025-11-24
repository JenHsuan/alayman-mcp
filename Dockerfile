# Use Python 3.11 as base image (matching .python-version)
FROM python:3.11-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies in a virtual environment (without the project itself)
# This layer is cached separately from project code changes
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# Copy the rest of the application
COPY . .

# Install the project in non-editable mode
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable --no-dev

# Final runtime stage
FROM python:3.11-slim

# Install uv (needed for `uv run`)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application files
COPY --from=builder /app/server.py /app/
COPY --from=builder /app/pyproject.toml /app/

# Copy .env file if it exists (for environment variables)
# Note: For production, consider using Docker secrets or environment variables instead
RUN --mount=type=bind,source=.,target=/tmp/context \
    cp /tmp/context/.env* ./ 2>/dev/null || true

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Run the server
CMD ["uv", "run", "server.py"]
