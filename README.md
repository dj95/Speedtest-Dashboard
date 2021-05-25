<h1 align="center">Speedtest Dashboard 📈</h1>

<p align="center">
  Monitor your internet bandwidth.
  <br><br>
  This repository provides a small application that is able to run speedtests in an interval
  and create Prometheus metrics from it. It also contains a docker-compose configuration with
  Prometheus and Grafana, to quickly spin up the dashboard.
</p>


## 📦 Requirements

- 🐳 Docker
- 🐙 docker-compose


## 🚀 Usage / Installation

Just clone the repository and run `docker-compose up -d`. The speedtest will run
every 30 minutes per default. If you wish to configure the interval, set the 
`INTERVAL_SECONDS` environment variable with the requested timeout in seconds
in the docker-compose.yml for the metricsserver.

After starting the containers, make sure they are running properly with `docker ps`.
Then open the browser at `localhost:3000` and login with the Grafan default credentials
(admin:admin). Configure a new prometheus data source with url set to `prometheus:9090`.

When the data source is configured, wait 1-2 minutes until the first speedtest was finished
and create a new dashboard in grafana. The following metrics are available from the speedtest:

- download_speed
- upload_speed
- ping_latency


## 🤝 Contributing

If you are missing features or find some annoying bugs please feel free to submit an issue or a bugfix within a pull request :)
