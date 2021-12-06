import logging
import os
import sys
from time import sleep

import pandas as pd
import sqlalchemy
from psycopg2._psycopg import AsIs
from sqlalchemy import create_engine, text
from psycopg2 import sql
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from imdb_analyser.data_classes.DataClass import DataClass

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s]  [%(levelname)s] %(message)s')


def read_db_config():
    """
    Read database configuration parameters from environment variables.
    Program will be stopped in case database password and database which should be connected to are omitted.
    :return:
    """
    host = str(os.getenv("DB_HOST", "localhost"))
    port = int(os.getenv("DB_PORT", 5432))
    user = str(os.getenv("DB_USERNAME", "admin"))
    database = os.getenv("DB_DATABASE")
    password = os.getenv("DB_PASSWORD")
    if not password or not database:
        logging.error(
            "You must provide a password and a database to access the database using environment variables "
            "DB_PASSWORD and DB_DATABASE!")
        sys.exit(1)
    return host, port, user, str(database), str(password)


def delete_all_data():
    """
    Delete all data in the database.

    :return: True if deletion was successful, False otherwise
    """
    deletion_order = ["public.movie_cast", "public.movie_genre", "public.award", "public.movie", "public.medium_type", "public.genre", "public.award_category", "public.actor"]
    with db_engine.connect():
        for table in deletion_order:
            try:
                logging.info("Deleting table %s...", table)
                db_engine.execute(f"DELETE FROM {table};")
                logging.info("Successfully deleted table %s", table)
            except Exception as err:
                logging.warning("Could not delete table %s", table, err)
                return False
    return True

def is_table_empty(table_name):
    """
    Check if a table is empty.

    :param table_name:
    :return:
    """
    # check whether this table exists or not to prevent SQL Injection attacks
    if not db_all_tables.loc[table_name:"table_name"].empty:
        logging.warning("Possible SQL Injection attack! It was attempted too query a non-whitelisted table! Provided table name: %s", table_name)
        return False
    result = pd.read_sql(f"SELECT 0 FROM {table_name} LIMIT 1", db_engine)
    return result.empty


def query(query_str, query_params=None):
    """
    Query database.

    :param query_str: query string
    :type query_str: str
    :param query_params: parameters for query
    :type query_params: dict
    :return: DataFrame containing result set
    """

    try:
        result = pd.read_sql(query_str, db_engine, params=query_params)
    except SQLAlchemyError as exc:
        logging.warning("Could not connect to database. Error: %s. Query %s with params %s failed!", exc, query_str, str(query_params))
    return result


def insert_into_db_table(df, data_class):
    """
    Insert data into database table.

    :param df: Dataframe with values to be inserted. Structure MUST match the SQL database table!
    :type df: pd.DataFrame
    :param data_class: a data class (e.g. Actor, Movie etc.)
    :type data_class: DataClass
    :return:
    """
    # get database table name and column configuration for given data class
    tab_name = data_class.db_table_name()
    column_config = data_class.db_column_config()
    # insert data in dataframe into specified database table
    logging.info("Inserting into table \"%s\"...", tab_name)
    try:
        df.to_sql(tab_name, db_engine, db_schema, if_exists="append", method=None, index=False, dtype=column_config)
        logging.info("Successfully inserted %d row(s) into table \"%s\"", df.shape[0], tab_name)
        return True
    except SQLAlchemyError as exc:
        logging.warning("Failed to insert %s row(s) into table \"%s\".", str(df.shape[0]), str(tab_name), exc_info=True)
        return False



db_host, db_port, db_user, db_database, db_password = read_db_config()
db_schema = "public"
db_enigne = None
db_con_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
db_engine = create_engine(db_con_str, pool_pre_ping=True, connect_args={'connect_timeout': 1})
success = False
retry_seconds = 1
max_retry_seconds = 30
while not success:
    try:
        logging.info("Trying to connect to database %s at %s:%s as user %s.", db_database, db_host, str(db_port), db_user)
        db_engine.connect()
        success = True
        logging.info("Successfully connected to database %s at %s:%s as user %s.", db_database, db_host, str(db_port), db_user)
    except SQLAlchemyError as exc:
        success = False
        logging.warning("Failed to connect to database %s at %s:%s as user %s. Error: %s. Retrying in %s second(s)...", db_database, db_host, str(db_port), db_user, exc, str(retry_seconds))
        # exponential backoff for retrying to connect to the database (blocking at the moment)
        new_retry_sec = retry_seconds * 2
        if new_retry_sec >= max_retry_seconds:
            new_retry_sec = max_retry_seconds
        retry_seconds = new_retry_sec
        sleep(retry_seconds * 3)

db_all_tables = query(query_str="SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
"""
Database engine. Single engine used for insertion and selection of data.
"""
