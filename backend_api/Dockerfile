# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install system dependencies (for Geopandas/Shapely if needed later)
# RUN apt-get update && apt-get install -y libgdal-dev

# Copy requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
