from os import getenv

VARS = {
    "RUN_TYPE": getenv("RUN_TYPE", "DEV"),
    "PROD_MYSQL_HOST": getenv("PROD_MYSQL_HOST"),
    "PROD_MYSQL_PORT": int(getenv("PROD_MYSQL_PORT", "3306")),
    "DEV_MYSQL_HOST": getenv("DEV_MYSQL_HOST"),
    "DEV_MYSQL_PORT": int(getenv("DEV_MYSQL_PORT", "3306")),
    "MYSQL_SCH": getenv("MYSQL_SCH"),
    "MYSQL_USER": getenv("MYSQL_USER"),
    "MYSQL_PASS": getenv("MYSQL_PASS"),
    "VENDOR_BASE_URL": getenv("VENDOR_BASE_URL")
}