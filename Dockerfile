# base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files into the container
COPY ./src /app/src

# Expose the app port
EXPOSE 80

# Run command
CMD uvicorn src.main:app --host 0.0.0.0 --port 80