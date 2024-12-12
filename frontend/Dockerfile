# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to avoid Python buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Expose port 3000 for the frontend Flask application
EXPOSE 3000

# Set the command to run the Flask app
CMD ["python", "frontend.py"]
