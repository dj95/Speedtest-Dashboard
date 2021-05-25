FROM debian:buster

# do not prompt when installing apt packages
ENV DEBIAN_FRONTEND "noninteractive"

# directly print the output from python
ENV PYTHONUNBUFFERED=1

# install prerequesites for installing speedtest
RUN apt update \
 && apt install -y \
        curl \
        python3 \
        python3-pip \
 && rm -rf /var/lib/apt/lists/*

# install the speedtest cli
RUN pip3 install speedtest-cli

# install the library for the prometheus client
RUN pip3 install prometheus-client

# create the directory in which the app lives
RUN mkdir -p /app

# copy the source code
COPY ./main.py /app/main.py

# start in the directory, where the source code is
WORKDIR /app

# use python 3 to start applications
ENTRYPOINT ["/usr/bin/python3"]

# run our metrics application
CMD ["./main.py"]
