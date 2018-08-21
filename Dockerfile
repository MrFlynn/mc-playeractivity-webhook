FROM alpine:latest
LABEL MAINTAINER="Nick Pleatsikas <nick@pleatsikas.me>"

# Install Python 3 and update pip.
RUN apk update \
    && apk add python3 \
    && pip3 install --upgrade pip

# Copy contents and enter working directory.
COPY . /app
WORKDIR /app

# Install application requirements.
RUN pip3 install -r requirements.txt

# Volume for accessing server configurations and files.
VOLUME [ "/server" ]

# Environment variable corresponding name of configuration file.
ENV CONFIG_FILE="config.ini"

# Command to run application.
CMD [ "python3", "main.py" ]
