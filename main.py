#!/usr/bin/env python3


import os
import json
import subprocess
import time

from prometheus_client import start_http_server, Gauge


def run_speedtest():
    """Run the speedtest and decode the result."""
    # run the speedtest with --json flag
    comp = subprocess.Popen(
        ['speedtest --json'],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # get the output from the process
    output_str, _ = comp.communicate()

    # parse the response and return it
    return json.loads(output_str)


def update_metrics(latencyGauge, downloadGauge, uploadGauge):
    """Run the speedtest and update metrics accordingly."""
    # run the speedtest
    res = run_speedtest()

    # get the single values from the response
    ping = res["ping"]
    upload = res["upload"]
    download = res["download"]
    server_name = res["server"]["name"]

    # update the metrics with the response values
    latencyGauge.labels(server_name).set(ping)
    uploadGauge.labels(server_name).set(upload)
    downloadGauge.labels(server_name).set(download)


def main():
    """Run main application code."""
    print(':: starting speedtest metrics server')

    # use Gauge to record the metrics
    labels = ['server_name']

    # configure the metrics we want to measure
    latencyGauge = Gauge('ping_latency', 'Ping Latency in ms', labels)
    downloadGauge = Gauge('download_speed', 'Download speed in bytes', labels)
    uploadGauge = Gauge('upload_speed', 'Upload speed in bytes', labels)

    # start the prometheus web server
    start_http_server(8080)

    # get the timeout interval for running the speedtest from the env
    timeout = os.environ.get('INTERVAL_SECONDS')

    # default to 1800 seconds if it is not set
    if timeout is None:
        timeout = '1800'

    # parse the timeout
    try:
        timeout = int(timeout, 10)
    except ValueError:
        timeout = 1800

    print(':: using timeout: {0} sec'.format(timeout))

    # run indefinetly
    while True:
        # update the metrics
        update_metrics(latencyGauge, downloadGauge, uploadGauge)

        # wait 30 minutes
        time.sleep(timeout)


if __name__ == '__main__':
    main()
