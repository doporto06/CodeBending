# Use Python 3.10 slim image
FROM python:3.10-slim

# Install system dependencies including Java JRE 17, Maven, and build tools
RUN apt-get update && apt-get install -y \
    openjdk-17-jre \
    maven \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p instance uploads ejerciciosPropuestos ejerciciosEstudiantes enunciadosEjercicios

# Initialize database
RUN python crear_db.py

# Expose port 3000
EXPOSE 3000

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_DEBUG=production

# Run the application
CMD ["python", "main.py"]