## Overview

A template for building a modern Python function in AWS lambda. 

The template demonstrates how to build and test a lambda function which runs HTTP and AWS actions concurrently with fast and cheap execution. The `src/` directory contains two example scripts which scrape bitcoin news from online sources and publish aggregated documents to S3. The output of the scripts is simple but they demonstrate a pattern for concurrent Python using [asyncio](https://docs.python.org/3/library/asyncio.html), [aiohttp](https://docs.aiohttp.org/en/stable/) and [aiobotocore](https://github.com/aio-libs/aiobotocore). 

The main lambda handler in `src/main.py` demonstrates how to run two asynchronous scripts concurrently while handling exceptions. An exception in one script will not prevent another script from running to completion. If any exception occurs then a global exception will be raised at the end of the function execution with a detailed traceback for debugging purposes. 

## Setup 

Clone this repository and install [Python 3.8+](https://www.python.org/downloads/). Then, create an isolated Python environment at the root of the project using virtualenv:

```
python3 -m venv venv
```

Activate the virtual environment:

```
source venv/bin/activate
```

You'll also need to configure your IDE to use the virtual environment (this is auto configured in VS Code by the `.vscode/settings.json` file).

## Install 

Install the Python modules required for development: 

```
pip -r install requirements-dev.txt
pip -r install requirements-prod.txt
```

If the virtual environment is activated then the Python modules will be installed inside a local `site-packages` directory. This will help to keep the project isolated from other Python projects on your machine. 

## Run the tests

This project uses `pytest` to run a suite of integration tests. These tests are designed to run as much application code as possible and they mock only the external HTTP and AWS calls. The tests use [aioresponses](https://github.com/pnuckowski/aioresponses) to mock async HTTP requests and the builtin module `unittest` to patch the aiobotocore module. Run the tests:

```
pytest
```

You can run the debugger in VS Code by setting a breakpoint and running the `Python: Module` launch configuration. 

## Deployment

In order to deploy this project to AWS lambda you'll need to zip the contents of the `src/` directory and include any external Python dependencies required in production. Run:

```
make package
```

This will make a fresh install of the production requirements into a `dist/` directory and will copy in the contents of the `src/` directory. The `dist/` directory is zipped to produce `dist.zip` which can be deployed to AWS lambda by uploading to S3 or through the AWS console. 

> For a lighter deployment package you can configure a [lambda layer with aiobotocore installed](https://github.com/keithrozario/Klayers/blob/master/deployments/python3.8/arns/eu-west-1.csv). The aiobotocore and aiohttp dependencies can then be removed from `requirements-prod.txt`. 