# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code, excluding the specified files and directories
COPY . .
RUN rm -rf database static admin_list.json .venv

# Add metadata labels
LABEL maintainer="WeepingDogel <weepingdogel@gmail.com>"
LABEL version="1.0"
LABEL description="Docker image for TinyGallery-Backend application"

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME TinyGallery-Backend

# Ensure run.sh is executable
RUN chmod +x run.sh

# Run the script
CMD ["./run.sh"]
