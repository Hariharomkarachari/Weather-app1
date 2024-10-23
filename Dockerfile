# Use Python 3.11.4 slim Debian Bullseye as the base image
FROM python:3.11.4-slim-bullseye

# Set environment variable to ensure Python output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED 1

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

ENV DJANGO_SETTINGS_MODULE=weather_app.settings

# Set the working directory in the container
WORKDIR /home/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 to allow external access to the application
EXPOSE 8000
