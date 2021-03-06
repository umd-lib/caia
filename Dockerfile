# Dockerfile for the generating caia application Docker image
#
# To build:
#
# docker build -t docker.lib.umd.edu/caia:<VERSION> -f Dockerfile .
#
# where <VERSION> is the Docker image version to create.

FROM python:3.8.2-slim

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean

# Create a user for the app.
RUN addgroup --gid 9999 app && \
    adduser --uid 9999 --gid 9999 --disabled-password --gecos "Application" app && \
    usermod -L app

USER app

# Make a subdirectory in the home directory for the application and make in the
# work directory
RUN mkdir /home/app/caia

# Configure the main working directory. This is the base
# directory used in any further RUN, COPY, and ENTRYPOINT
# commands.
WORKDIR /home/app/caia

# Add /home/app/.local/bin where the Python dependencies will be installed
# to the PATH
ENV PATH=/home/app/.local/bin:$PATH

# Copy the requirements.txt file holding the Python packages to install and
# run "pip install". This is a separate step so the dependencies will be cached
# unless changes to the file are made.
COPY --chown=app:app requirements.txt /home/app/caia/

RUN cd /home/app/caia && \
    pip install -r requirements.txt && \
    cd ..

# Copy the main application
ENV PYTHONUNBUFFERED=1
COPY  --chown=app:app . /home/app/caia

# Install the main application
RUN cd /home/app/caia && \
    pip install .
