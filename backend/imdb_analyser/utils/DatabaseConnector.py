import logging
import os
import sys

import pandas as pd
import sqlalchemy
from psycopg2._psycopg import AsIs
from sqlalchemy import create_engine, text
from psycopg2 import sql

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

    return pd.read_sql(query_str, db_engine, params=query_params)


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
    except Exception as exc:
        logging.warning("Failed to insert %s row(s) into table \"%s\".", str(df.shape[0]), str(tab_name), exc_info=True)
        sys.exit(45)
    logging.info("Successfully inserted %d row(s) into table \"%s\"", df.shape[0], tab_name)


db_host, db_port, db_user, db_database, db_password = read_db_config()
db_schema = "public"
db_engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}")
db_all_tables = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'", db_engine)
"""
Database engine. Single engine used for insertion and selection of data.
"""
