# Use an official Ubuntu runtime as a base image
FROM python:3.9

LABEL authors="tom"

ENV VIRTUAL_ENV=/opt/venv

COPY ./* ./
COPY entrypoint.sh ./entrypoint.sh
COPY ./attendant ./attendant
COPY ./scripts ./scripts
COPY ./docker.env ./.env

# Install required dependencies
RUN apt-get update && apt-get install -y \
    android-tools-adb \
    android-tools-fastboot \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv $VIRTUAL_ENV \
    && pip install elemental_tools==0.0.1.8
##    && echo "source $VIRTUAL_ENV/bin/activate" >> ~/.bashrc \

# Expose the port
EXPOSE 5037
EXPOSE 3001

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
