#!/bin/bash
### Make sure to have added the MYSQL_USER and MYSQL_PASS environment variables before running this script
source env.sh
source venv/bin/activate
python3 atlas/main.py