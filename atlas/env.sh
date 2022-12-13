# RUN_TYPE can be DEV or PROD and will use the corresponding HOST and PORT but will keep everything else the same
# RUN_TYPE accepts two values DEV and PROD, DEV uses the RDS MySQL instance and loads the final matches in the database.
# PROD utilized the Doximity MySQL instance and skips the loading of the final matches.
export RUN_TYPE=DEV

export PROD_MYSQL_HOST=candidate-coding-challenge.dox.pub
export PROD_MYSQL_PORT=3316

export DEV_MYSQL_HOST=ls-2a4a94a11744d5162e7a5974d3825f6af43e9cdc.cu2sawnxctut.us-east-1.rds.amazonaws.com
export DEV_MYSQL_PORT=3306

export MYSQL_SCH=data_engineer
export MYSQL_USER=EXAMPLE_USER ## CHANGE ME
export MYSQL_PASS=EXAMPLE_PASS ## CHANGE ME

export VENDOR_BASE_URL=https://de-tech-challenge-api.herokuapp.com/api
export DOX_BATCH_PERCENTAGE=10
export API_BATCH_PERCENTAGE=10
export API_VERSION=1