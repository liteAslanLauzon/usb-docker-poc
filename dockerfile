FROM python:3.11-slim

# Install uv (single binary installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set working directory
WORKDIR /app

# Copy only project files
COPY pyproject.toml /app/
COPY uv.lock /app/     
COPY main.py /app/

# Install dependencies with uv
RUN /root/.cargo/bin/uv pip install --system --no-cache .

# Run the Python script
CMD ["python", "main.py"]
