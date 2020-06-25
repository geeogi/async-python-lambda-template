# AWS lambda with asynchronous Python using asyncio, aiohttp and aiobotocore 

A template for building a high-performance Python function in AWS lambda. 

## Overview

This template demonstrates how to build and test a lambda function which runs HTTP requests and AWS actions concurrently to achieve fast and cheap lambda execution. The [src/](./src) directory contains two example scripts which scrape bitcoin news from online sources and publish aggregated documents to S3. The output of the scripts is simple but they demonstrate a pattern for concurrent Python using [asyncio](https://docs.python.org/3/library/asyncio.html), [aiohttp](https://docs.aiohttp.org/en/stable/) and [aiobotocore](https://github.com/aio-libs/aiobotocore). You can see an example of the documents produced by this lambda in the test [fixtures](./tests/fixtures/documents).

The main lambda handler in [src/main.py](src/main.py) demonstrates how to run any number of asynchronous scripts concurrently while handling exceptions gracefully. If an exception occurs within an individual script then a global exception will be raised only after all other scripts have completed. A detailed traceback is logged for debugging purposes. 

## Setup 

Clone this repository and install [Python 3.8+](https://www.python.org/downloads/). Then, create an isolated Python environment at the root of the project using virtualenv:

```
python3 -m venv venv
```

Activate the virtual environment:

```
source venv/bin/activate
```

You'll also need to configure your IDE to use the virtual environment (this is auto configured in VS Code by the [.vscode/settings.json](.vscode/settings.json) file).

## Install 

Install the Python modules required for development: 

```
pip -r install requirements-dev.txt
pip -r install requirements-prod.txt
```

The Python modules will be installed inside a local `site-packages` directory maintained by the virtual environment. This will help to keep the project isolated from other Python projects on your machine. 

## Run the tests

This project uses `pytest` to run a suite of integration tests which are designed to run as much application code as possible while mocking the external HTTP and AWS calls. The tests use [aioresponses](https://github.com/pnuckowski/aioresponses) to mock async HTTP requests and the builtin module `unittest` to patch the aiobotocore module. Run the tests:

```
pytest
```

You can run the debugger in VS Code by setting a breakpoint and running the `Python: Module` launch configuration. 

## Deployment

Provision a new lambda component on AWS using the [AWS console](https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html) or via [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html) template. 

In order to deploy this project to your AWS lambda component you'll need to zip the contents of the `src/` directory and include any 3rd party Python modules required in production. Run:

```
make package
```

This will make a fresh install of the production requirements into a `dist/` directory and will copy in the contents of the `src/` directory. The `dist/` directory is zipped to produce `dist.zip` which can be deployed to AWS lambda through the AWS console or by uploading to S3. 

> For a smaller deployment package you can configure a [lambda layer with aiobotocore installed](https://github.com/keithrozario/Klayers/blob/master/deployments/python3.8/arns/eu-west-1.csv). The aiobotocore and aiohttp dependencies can then be removed from `requirements-prod.txt`. 

## Q&A

#### What's AWS lambda?

AWS lambda is a software environment which lets you run code without having to provision or manage you're own server. To develop a lambda you'll need to implement a function (the handler) that will be called when the lambda is invoked. 

Lambdas are connected to the AWS ecosystem and can be easily configured to run on a schedule or be triggered by a REST API call or by another AWS event such as SNS message or S3 upload. Lambda comes with a simple interface for monitoring performance and editing the function code on the fly. 

With AWS Lambda you pay only for the compute time you consume so if your code has a fast and efficient execution time then it can be very cheap to run. 