# High-performance AWS lambda with async Python 

_A template for building a high-performance Python function in AWS lambda using asyncio, aiohttp and aiobotocore. Perfect for a data processing pipeline._ 

## Features

- High-performance async Python 
- Runs in AWS lambda serverless environment λ 
- Integration tests with HTTP and AWS mocks
- CloudFormation template for AWS infrastructure deployment 
- Step-by-step guide to setup, install, test and deploy 

## Overview

This template demonstrates how to build and test a lambda function which runs HTTP requests and AWS actions concurrently to achieve fast and cheap execution. The [src/](./src) directory contains two example scripts which scrape bitcoin news from online sources and publish aggregated documents to S3. The output of the scripts is simple but they demonstrate a pattern for concurrent Python using [asyncio](https://docs.python.org/3/library/asyncio.html), [aiohttp](https://docs.aiohttp.org/en/stable/) and [aiobotocore](https://github.com/aio-libs/aiobotocore). You can see an example of the documents produced by this lambda in the test [fixtures](./tests/fixtures/documents).

This repository also includes a CloudFormation template which can be used to deploy the lambda and S3 infrastructure on AWS with appropriate IAM policies.

## Setup

Clone this repository and install [Python 3.8+](https://www.python.org/downloads/). Then, create an isolated Python environment at the root of the project using virtualenv:

```
python3 -m venv venv
```

Activate the virtual environment:

```
source venv/bin/activate
```

You'll also need to configure your IDE to use the virtual environment (this should be auto configured in VS Code by the [.vscode/settings.json](.vscode/settings.json) file).

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

## Infrastructure

To provision the lambda and S3 infrastructure on AWS you'll need to visit the CloudFormation service in the AWS console and upload the stack template declared in [template.json](template.json). This will create a lambda component and S3 bucket with appropriate IAM policies.

> The lambda will be configured to run Python 3.7 since it's not yet possible to deploy Python 3.8+ via CloudFormation using the ZipFile property. If you need Python 3.8+ you can update your lambda through the AWS console after it's been created or configure the lambda's Runtime and Code properties in the CloudFormation template using an S3 bucket. 

## Deployment

To deploy the source code to the lambda component you'll need to zip the contents of the `src/` directory and include any 3rd party Python modules required in production. Run:

```
make package
```

This will make a fresh install of the production requirements into a `dist/` directory and will copy in the contents of the `src/` directory. The `dist/` directory is zipped to produce `dist.zip` which can be deployed to the lambda component via upload in the AWS console.

> For a smaller deployment package you could configure a [lambda layer with aiobotocore installed](https://github.com/keithrozario/Klayers/blob/master/deployments/python3.8/arns/eu-west-1.csv). The aiobotocore and aiohttp dependencies can then be removed from `requirements-prod.txt`.

## Error handling 

The main lambda handler in [src/index.py](src/index.py) demonstrates how to run any number of scripts concurrently while handling exceptions gracefully. If an exception occurs within an individual script then a global exception will be raised only after all other scripts have completed. A detailed traceback is logged for debugging purposes.

## Invoke the lambda

The simplest way to invoke a lambda function is by creating and [firing a test event using the AWS console](https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html#get-started-invoke-manually). You can also, for example, configure [CloudWatch Events](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html) to trigger your lambda on a schedule (e.g. every 5 mins) or configure [API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html) to trigger it by HTTP request. 

## Q&A

#### Why use asynchronous Python? 

Async Python code can speed up the execution time of a script by performing I/O concurrently. While a synchronous Python script will perform network requests one by one, an asynchronous Python script is able to handle multiple network requests at a time which can have a significant benefit when many requests are made. 

A similar effect can be achieved with synchronous code using multithreading but the concurrent pattern with asyncio is often easier to understand and reason about, thanks to the explicit async/await syntax. 

If your script does not perform significant I/O then there likely won't be any benefit from using asynchronous code. 

#### Why use AWS lambda?

AWS lambda is a software environment that lets you run code without having to provision or manage your own server. To develop a lambda you only need to implement a function (the handler) to be called when the lambda is invoked.

Lambdas are connected to the AWS ecosystem and can be configured to run on a schedule or be triggered by HTTP request or by another AWS event such as SNS message or S3 upload. Lambda comes with an interface for monitoring performance and editing the function code on the fly.

With AWS Lambda you only pay for the execution time you consume so if your code is fast and efficient then it can often be cheaper to run than a traditional server instance.

## Contributing

Please raise an issue. Thanks. 

## License

MIT