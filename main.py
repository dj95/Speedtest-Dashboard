#!/usr/bin/env python3


import os
import json
import subprocess
import time
import sys
import _thread

from prometheus_client import start_http_server, Gauge
from pythonping import ping


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


def update_ping_thread(pingGauge, ping_dest):
    """Update the ping metrics with the ping to cloudflare."""
    # thread main loop
    while True:
        # ping the server
        response_list = ping(ping_dest, size=40, count=10)

        # set the average ms in the ping gauge
        pingGauge.labels(ping_dest).set(response_list.rtt_avg_ms)

        print(":: updated ping")

        # wait 60 seconds for the next update
        time.sleep(60)


def update_metrics_thread(latencyGauge, downloadGauge, uploadGauge, timeout):
    """Run the speedtest and update metrics accordingly."""
    # thread main loop
    while True:
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

        print(":: updated speedtest")

        time.sleep(timeout)


def main():
    """Run main application code."""
    print(':: starting speedtest metrics server')

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

    # get the ping destination
    ping_dest = os.environ.get('PING_DESTINATION')

    # use Gauge to record the metrics
    labels = ['server_name']

    # configure the metrics we want to measure
    latencyGauge = Gauge('ping_latency', 'Ping Latency in ms', labels)
    downloadGauge = Gauge('download_speed', 'Download speed in bytes', labels)
    uploadGauge = Gauge('upload_speed', 'Upload speed in bytes', labels)
    if ping_dest is not None:
        pingGauge = Gauge('ping_custom', 'Custom ping latency in ms', labels)

    # start the prometheus web server
    start_http_server(8080)

    print(':: using timeout: {0} sec'.format(timeout))

    _thread.start_new_thread( update_metrics_thread, (latencyGauge, downloadGauge, uploadGauge, timeout,) )
    if ping_dest is not None:
        _thread.start_new_thread( update_ping_thread, (pingGauge, ping_dest) )

    while True:
        time.sleep(60)



if __name__ == '__main__':
    main()
