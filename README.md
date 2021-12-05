![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)

# IMDb Webscraping Project

## Table of Contents

- [IMDb Webscraping Project](#imdb-webscraping-project)
  - [Table of Contents](#table-of-contents)
  - [Getting started](#getting-started)
  - [Services](#services)
    - [Web application](#web-application)
      - [Frontend](#frontend)
      - [Backend](#backend)
    - [PostgreSQL](#postgresql)
  - [Requirements](#requirements)
  - [License](#license)


## Getting started
The application is deployed as a complete application stack. To make that work you need to have two things installed:
- [Docker](https://docs.docker.com/get-docker/): container runtime to run paravirtualized workloads (= container)
- [docker-compose](https://docs.docker.com/compose/install/): allows to deploy a stack of containers

Second, you need to clone this repository:
```bash
git clone https://github.com/Mushroomator/kpi-collection.git
```

Now move into the cloned repository
```bash
cd IMDb-Webscraping-Project
```
and deploy the stack on your local machine
```
docker-compose up
```
> Note: At first run this command will take some time as all containers must be downloaded first before they get started by the Docker engine.

You can check whether the deployment was successful by running `docker ps -a` which displays all currently running containers on the system.
As each of the deployed containers has a healthcheck configured to ensure the service runs as expected you can also the the current health status for a container using this command.
Wait a few seconds and run `docker ps -a` again and you should see the status of the containers going from *starting* to *healthy*. That's when every thing is ready to go.

You may now access pgAdmin on `http://localhost:80` and login as `admin` user using the password `simplepw` or access the web GUI for the application by visiting `http://localhost:5000`.

## Services
### Web application
#### Frontend
[React.js](https://reactjs.org/) application written in [TypeScript](https://www.typescriptlang.org/) using [Chakra UI component library](https://chakra-ui.com/). The frontend takes care of routing by using [React Router](https://reactrouter.com/) and will fetch required data from the API when needed.

#### Backend
The backend was written using Python 3.9. For simplicity [Flask](https://flask.palletsprojects.com/en/2.0.x/) was used to handle requests.

### PostgreSQL
Persistence is provided by a PostgreSQL database running inside of the container. The container exposes default port `5432` within the created user-defined Docker network so the [web app](#web-application) can access it using TCP. All data is persisted to the created volume `db-data`.


## Requirements
The Python backend relies on ordered dictionaries so a **Python version >= 3.7** is needed for the application to work correctly. The provided Docker image uses Python 3.9 as this is also used in the virtual environment.

## License
Copyright 2021 Thomas Pilz

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.