FROM qgis/qgis

# Set working directory inside the container
WORKDIR /app

# Update package list and install required system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and activate it
RUN python3 -m venv /app/venv

# Set environment variables for Python and Pip inside the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy the requirements file first (to optimize caching)
COPY requirements.txt .

# Install Python dependencies inside the virtual environment
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Load environment variables from the .env file (for local development)
ARG COPERNICUS_USERNAME
ARG COPERNICUS_PASSWORD
ENV COPERNICUS_USERNAME=$COPERNICUS_USERNAME
ENV COPERNICUS_PASSWORD=$COPERNICUS_PASSWORD

# Default command (optional)
CMD ["bash"]
