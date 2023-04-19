# Stock Oracle For All

## Description

Data oracle is a concept of a software aggregating from multiple data sources and expose the reliable data endpoint to data user in a solid and secure way. Data oracle solves the issue of single point of failure happens with traditional system with only one central node or database.

## Solution stack

-   **Mercury:** Extract transform load pipeline (built with Spark, Dagster). Spark is used as computing engine on large stock data retrieved from API and Dagster is used for scheduling and orchestrating.

## Development guideline

### Setup virtual environment

```
virtualenv . ; ./bin/activate
```

### Install packages

```
make install
```

#### Using pipenv

The project is managed using `pipenv`. To install packages, please do:

```
pipenv install
```

To install new packages, please do:

```
pipenv install <package>
```

#### Using requirements.txt

To write the packages version into `requirements.txt`, run the command

```
make sync
```

# Set up

1. install Docker and docker-compose
1. set active directory to project root
1. docker-compose up
