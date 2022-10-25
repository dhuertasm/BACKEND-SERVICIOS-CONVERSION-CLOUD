# BACKEND-SERVICIOS-CONVERSION-CLOUD

<!--
## Table of Contents
* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [API](#api)
* [System errors](#system-errors)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)
-->
<!-- ABOUT THE PROJECT -->
## About The Project

This project is a basic microservice for tangelo leasing etl project

### Built With
* Language: Python3
* Framework: Flask
* Database: PostgreSQL
* Services: Redis, celery
* container:  


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.


### Installation 

1. Install Virtualenv and activate it
```sh
$ virtualenv -p python3 venv
```
```sh
$ source venv/bin/activate
```
2. Install requirements.txt
```sh
$ pip3 install -r requirements.txt
```
### Execution

### flask Server

create user 

```sh
$  flask run --reload
```

### celery 

```sh
$  celery -A core.celery worker --beat --loglevel=info
```


## Running whit docker-compose for different envs

* Export your enviroment as environ variable
    ```shell
          export BROKER_URL='redis://127.0.0.1:6379'
    ```

* Run your docker compose with this command in /docker/local
    ```shell
        sudo docker-compose up --build   
    ```

    * **Note** if build is not required you can ommit the `--build`

    
<!-- API -->
## Pruebas

En el archvio *test_plan_escenario_1.jmx*  y *test_plan_escenario_2.jmx* se encuentra
los test de Jmeter para las pruebas de estres, carga del api converter format.


<!-- ARCHITECTURE -->
## Architecture


<!-- CONTACT -->
## Contact


