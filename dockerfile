FROM python:3.13-slim-bookworm

# Setup working directory
WORKDIR /app

# Install essential system packages for OpenCV to function properly
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
 && rm -rf /var/lib/apt/lists/*

# Install uv by Astral
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Copy project files
COPY pyproject.toml /app/
COPY uv.lock /app/
COPY main.py /app/

# Install Python dependencies into system environment
RUN uv pip install --system --no-cache .

# Run the application
CMD ["python", "main.py"]
