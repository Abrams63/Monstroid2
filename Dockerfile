# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code into the container
COPY backend/ ./backend/

# Copy the site directory into the container
COPY site/ ./site/

# Expose port 8000 for the application
EXPOSE 8000

# Run the application using uvicorn
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]