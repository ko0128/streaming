FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1

# set the working directory in the container
WORKDIR /client

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

EXPOSE 4000

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python","-u", "./client.py" ]