#!/bin/bash

### Assumptions
###  - Python 3.6 or greater is installed
###  - virtualenv is installed

virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt