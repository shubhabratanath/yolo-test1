#FROM python:3.7.5
FROM python:3.7-slim-bullseye

COPY . /home/user
WORKDIR /home/user

RUN apt-get update && apt-get -y install python3-pip libgl1 libglib2.0-0
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install flask
RUN pip3 install flask_cors
RUN pip3 install ultralytics

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]
