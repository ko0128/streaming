FROM python:3.8-slim-buster

# set the working directory in the container
WORKDIR /server

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .
EXPOSE 7000

# command to run on container start
CMD [ "python","-u", "./server.py" ]