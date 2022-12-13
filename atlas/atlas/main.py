from datetime import datetime
import typer

from setup import start_logger
from api import UsersV1
from dox import DoxMySQLRead, DoxMySQLWrite
from match import MatchMaker
from utils import Timer, Sample, DDL_OUTPUT
from config import VARS

'''
Typer cli implementation for easily taking in command line arguments, this could
have been mimicked with argparse. The ease of implementation and out of the box
features were worth the dependancy on the external library in my mind.
'''

def main(
    run_date: datetime = typer.Argument(
        "2017-02-02",
        formats=["%Y-%m-%d"],
        help="Please pass through a run_date if you would like to override the default."
    ),
    dox_batch_percentage: int = typer.Argument(
        10,
        min=1,
        max=100,
        envvar="DOX_BATCH_PERCENTAGE",
        help="Please enter a batch percentage for the Doximity MySQL instance, between 1 and 100, if you would like to override the default."
    ),
    api_batch_percentage: int = typer.Argument(
        10,
        min=1,
        max=100,
        envvar="API_BATCH_PERCENTAGE",
        help="Please enter a batch percentage for the Vendor API between 1 and 100 if you would like to override the default."
    ),
    vendor_base_url: str = typer.Argument(
        "https://de-tech-challenge-api.herokuapp.com/api",
        envvar="VENDOR_BASE_URL",
        help="Please enter the base url for the Vendor API if you would like to override the default, example: https://example.com/api - Note: don't enter the API Version Number here."
    ),
    api_version: int = typer.Argument(
        1,
        min=1,
        max=100,
        envvar="API_VERSION",
        help="Please enter a valid API version for the Vendor API if you would like to override the default. Not implemented yet as there is only one version of the API."
    )
) -> None:

    logger = start_logger()

    t = Timer()
    t.start()

    mysql_host = VARS[f"{VARS['RUN_TYPE']}_MYSQL_HOST"]
    mysql_port = VARS[f"{VARS['RUN_TYPE']}_MYSQL_PORT"]
    mysql_sch = VARS['MYSQL_SCH']
    mysql_user = VARS['MYSQL_USER']
    mysql_pass = VARS['MYSQL_PASS']

    external_users = UsersV1(
                base_url=vendor_base_url,
                percentage=api_batch_percentage
            )
    internal_users = DoxMySQLRead(
                host=mysql_host,
                port=mysql_port,
                database=mysql_sch,
                username=mysql_user,
                password=mysql_pass,
                run_date=run_date,
                percentage=dox_batch_percentage
            )
    internal_loader = DoxMySQLWrite(
                host=mysql_host,
                port=mysql_port,
                database=mysql_sch,
                username=mysql_user,
                password=mysql_pass,
            )

    mm = MatchMaker(
                internal_users=internal_users, 
                external_users=external_users
            )
    

    ### Starts loading the queues and matching records from the two data sources. Returns the
    ### full list of matched records ready to insert into the database.
    logger.debug("Starting queueing process.")
    merged_list = mm.main()

    ### Returns the output to get printed at the end of the run for Total Matches and formatted samples.
    total_matches_output = mm.get_total_matches_output()
    samples_output = mm.get_samples_output()

    if VARS['RUN_TYPE'] == 'DEV':        
        ### Creates the user_match table in MySQL if it doesn't already exist.
        internal_loader.build_user_match_table()
        logger.debug("Loading user_match table into MySQL")

        ### Keeps the runs idempotent by removing anything previously ran with the same run_date.
        internal_loader.rerun()
        logger.debug(f"Removing any records with a run_date of: {run_date}")

        ### Loads the list of dictionaries into MySQL as effeciently as possible right now.
        internal_loader.list_of_dict_to_sql('user_match', merged_list)
        logger.debug(f"Loaded matches into user_match table.")

    elif VARS['RUN_TYPE'] == 'PROD':
        logger.debug("Run_Type is PROD, skipping loading data into MySQL.")

    t.stop()

    print(str(t))
    print("")
    print(total_matches_output)
    print("")
    print(samples_output)
    print("")
    print(DDL_OUTPUT)

if __name__ == '__main__':
    typer.run(main)