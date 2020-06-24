## Asyncio HTTP + AWS Lambda

The project uses [aiohttp](https://docs.aiohttp.org/en/stable/) to make asynchronous HTTP requests and [aiobotocore](https://github.com/aio-libs/aiobotocore) to perform asynchronous AWS actions. The function will run multiple HTTP requests and AWS S3 requests concurrently making it faster and cheaper. 

Logic is divided into scripts which are run concurrently in the main Lambda handler. An exception in one script will not prevent another script from running to completion. If any exception occurs then a global exception will be raised at the end of the function execution with a detailed traceback.

## Setup environment 

Install [Python 3.8+](https://www.python.org/downloads/). Then, create an isolated Python environment at the root of the project using virtualenv:

```
python3 -m venv venv
```

Activate the virtual environment:

```
source venv/bin/activate
```

Python modules will be installed inside a local `site-packages` directory which should keep this project isolated from other Python projects on your machine. You'll also need to configure your IDE to use the virtual environment when running/debugging the project (this is auto configured in VS Code by the `.vscode/settings.json` file).

## Install 

Install the Python dependencies required for development: 

```
pip -r install requirements-dev.txt
pip -r install requirements-prod.txt
```

## Run the tests

This project uses `pytest` to run a suite of integration tests. These tests are designed to run as much application code as possible and they mock only the external HTTP and AWS calls. The tests use [aioresponses](https://github.com/pnuckowski/aioresponses) to mock async HTTP requests and the builtin module `unittest` to patch the aiobotocore module. Run the tests:

```
pytest
```

You can run the debugger in VS Code by setting a breakpoint and running the `Python: Module` launch configuration. 

## Package

In order to deploy this project to AWS Lambda you'll need to zip the contents of the `src/` directory and include any external Python dependencies required in production. Run:

```
make package
```

This will make a fresh install of the production requirements into a `dist/` directory and will copy in the contents of the `src/` directory. The `dist/` directory is zipped to produce `dist.zip` which can be deployed to AWS Lambda by uploading to S3 or through the AWS console. 

> For a lighter deployment package you can configure a [lambda layer with aiobotocore installed](https://github.com/keithrozario/Klayers/blob/master/deployments/python3.8/arns/eu-west-1.csv). The aiobotocore and aiohttp dependencies can then be removed from `requirements-prod.txt`. 