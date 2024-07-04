# Use an official Python runtime as a parent image
FROM python:3.11 as base

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .. .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --timeout=1200 -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python3", "app.py"]
