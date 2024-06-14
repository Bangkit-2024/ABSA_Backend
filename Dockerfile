# Use the official Python image from the Docker Hub
FROM python:3.11

# Set environment variables to prevent Python from writing .pyc files and to prevent buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV STAGE PROD

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
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt install git-lfs
RUN git clone https://huggingface.co/kaylaisya/absa-polarity /app/services/absa/model/large_model/absa-polarity
RUN git clone https://huggingface.co/kaylaisya/absa-aspect /app/services/absa/model/large_model/absa-aspect
RUN git clone https://huggingface.co/indobenchmark/indobert-base-p1 /app/services/absa/model/large_model/indobert-base-p1
RUN ls -a


# Expose port 8000 to the outside world
EXPOSE 8000

# CMD ["python","manage.py","makemigrations"]
# CMD ["python","manage.py","migrate"]
# Set the default command to run the Django application using gunicorn
CMD pyhton manage.py runserver
