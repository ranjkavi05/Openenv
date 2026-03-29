# ── Build stage ──────────────────────────────────
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501
# Expose FastAPI port
EXPOSE 8000

# Copy project files
COPY . .

# Make sure start.sh is executable
RUN chmod +x start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/state || exit 1

# Run the startup script
ENTRYPOINT ["./start.sh"]
