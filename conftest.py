import os
import sys

"""
The src directory is included in PATH when the Python interpreter is invoked by src/handler.py
However it's not included when the interpreter is invoked by PyTest, so we append it manually
"""
sys.path.append(f"{sys.path[0]}/src")

"""
Mock AWS credentials during tests
"""
os.environ["AWS_ACCESS_KEY_ID"] = "MOCK_ID"
os.environ["AWS_SECRET_ACCESS_KEY"] = "MOCK_KEY"
os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
