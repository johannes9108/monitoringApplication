# Monitoring Application
## Final project in the course Systemutveckling med Python
* Create a monitoring application that can monitor the CPU, memory, and disk usage of a computer.
* The application should be able to set alarms for when the usage exceeds a certain percentage.
* The application should be able to log the alarms to a file.
* The application should be able to remove alarms. 
* The application should be able to write alarms to a file in JSON format.
* The application should be able to handle incorrect input without crashing.
* The application should be written with functions.
* The application should use object-oriented programming where it fits.
* The application should be written with functional programming in at least one place. For example, when sorting alarms before displaying them.
## Pylint
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
## Black formatter
* In settings.json
```
"editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "always"
    },
```
## Prometheus config
* docker run -d --name prometheus -v /c/chasAcademy/Systemutveckling-Python/monitoringApplication/prometheus.yml:/opt/bitnami/prometheus/conf/prometheus.yml bitnami/prometheus:latest
* For Windows: docker run -d -p 8090:8090 --name prometheus -v "C:\\chasAcademy\\Systemutveckling-Python\\monitoringApplication\\prometheus.yml:/opt/bitnami/prometheus/conf/prometheus.yml" bitnami/prometheus:latest
* du -hs data/wal/00000000 - Check the size of the WAL file
* WAL file - Write Ahead Log file
* Use host.docker.internal instead of localhost - because localhost refers to the container itself.	