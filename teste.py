import boto3
import inspect
import simple_bot as module
import sys

def teste1():
    pass

def teste2():
    pass

def teste3():
    pass

print(inspect.getmodulename(__file__))
print(inspect.getmembers(inspect.getmodulename(__file__), inspect.isfunction))
print(inspect.getmembers())