# Monitoring Application

## Goals for final project in the course Systemutveckling med Python
* Create a monitoring application that can monitor the CPU, memory, and disk usage of a computer.
* The application should be able to set alarms for when the usage exceeds a certain percentage.
* The application should be able to log the alarms to a file.
* The application should be able to remove alarms. 
* The application should be able to write alarms to a file in JSON format.
* The application should be able to handle incorrect input without crashing.
* The application should be written with functions.
* The application should use object-oriented programming where it fits.
* The application should be written with functional programming in at least one place. For example, when sorting alarms before displaying them.
## Usage
* Run the application with `python app.py`
* To use the options regarding monitoring, the `Start monitoring` option must be triggered once.
* Grana and Prometheus will be set up automatically when running the application but the user must set up their local Grafana/Prometheus docker containers.
* Prometheus CLient will be running on port 8000 and expose the metrics on `/metrics`.
* Prometheus server is running on port 9090 and the configuration file is located in the root directory.
* Grafana is running on port 3000 and to ![Grafana Set up](image.png "Grafana Set up")
## Configuration
### Pipenv
* To install the dependencies, run `pipenv install`
* Depending on the terminal, the command `pipenv shell` might be needed to activate the virtual environment.
### Prometheus/Grafana config
* To run Prometheus a custom configuration file is needed. The configuration file is located in the root directory and is named `prometheus.yml`. The most important setting is to find the correct target for the Prometheus server to scrape. The target is the IP address of the host machine. The configuration file should look like this because the metric endpoint is exposed locally on port 8000:
```yml
...
scrape_configs:
  - job_name: "cli_app"
    static_configs:
      - targets: ["host.docker.internal:8000"]
...
```
* docker run -d -p 8090:8090 --name prometheus -v {absolutePath}/monitoringApplication/prometheus.yml:/opt/bitnami/prometheus/conf/prometheus.yml bitnami/prometheus:latest
* {absolutePath} - Follow the standard for slashes for the operating system you are using:
  * Unix/Linus: /c/chasAcademy/Systemutveckling-Python
  * Windows: C:\\chasAcademy\\Systemutveckling-Python
* docker run -d -p 3000:3000 --name grafana grafana/grafana
* du -hs data/wal/00000000 - Check the size of the WAL file
* WAL file - Write Ahead Log file
* Use host.docker.internal instead of localhost - because localhost refers to the container itself.	
* [Prometheus Client](https://github.com/prometheus/client_python/blob/d7c9cd88c7f50097cd86869974301df7615bc9c0/prometheus_client/metrics.py#L264)
* http://localhost:9090/api/v1/query?query=up - Check if Prometheus is up
* http://localhost:8000/metrics
* https://prometheus.io/download/
* https://hub.docker.com/r/grafana/grafana
### Pylint
* [Pylint docs](https://pylint.readthedocs.io/en/latest/user_guide/messages/convention/invalid-name.html)
* In settings.json
```
pylint.showNotifications": "onWarning",
    "pylint.importStrategy": "fromEnvironment",
    "pylint.args": [
        "--max-line-length=120",
        "--module-naming-style=camelCase",
        "--variable-naming-style=camelCase",
        "--argument-naming-style=camelCase",
        "--function-naming-style=camelCase",
        "--method-naming-style=camelCase",
        "--attr-naming-style=camelCase",
        "--class-attribute-naming-style=camelCase",
        "--class-naming-style=PascalCase",
        "--disable=C0410,C0121"
    ],
```
### Black formatter
* In settings.json
```
"editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "always"
    },
```