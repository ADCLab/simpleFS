# Use the official Python 3.12 image as the base
FROM python:3.12-slim

# Set environment variables to ensure Python runs in production mode
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory in the container
WORKDIR /app

# Create the /data folder in the container (for file storage or uploads)
RUN mkdir /data

# Copy the FastAPI application code into the container
COPY app/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

