# Use the official Python image from the Docker Hub
FROM python:3.11

# Set environment variables to prevent Python from writing .pyc files and to prevent buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV STAGE DEV

# Set the working directory inside the container
WORKDIR /app


# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/
COPY . .

# Install the dependencies specified in the requirements.txt file
RUN pip install huggingface_hub
RUN pip install tensorflow==2.15.0
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory

RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Set the default command to run the Django application using gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "absa.wsgi:application"]
