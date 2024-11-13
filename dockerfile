# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Copy the local requirements.txt to the container at /app
COPY requirements.txt /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Set environment variables
# You can customize these as per your Flask app's needs
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port 5000 to allow external access to the app
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
