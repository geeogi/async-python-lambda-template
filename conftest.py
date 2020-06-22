import sys

"""
The src directory is included in PATH when the Python interpreter is invoked by src/handler.py
However it's not included when the interpreter is invoked by PyTest, so we append it manually
"""
sys.path.append(f"{sys.path[0]}/src")
