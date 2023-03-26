import os
import sqlite3
import time

import src.data as project_data
from os.path import exists
from sqlite3 import Error
import logging

__DB_TABLE_NAME__ = "datasets"


def create_connection(db_fp: str) -> (bool, str, sqlite3.Connection):
    logging.info(msg="Creating database connection...")
    conn: sqlite3.connect = None
    success: bool = False
    stderr: str = ""
    if not _database_exists(db_fp=db_fp):
        return _create_database(db_fp=db_fp)
    try:
        conn = sqlite3.connect(db_fp)
        success = True
        stderr = "No error"
    except Error as e:
        stderr = f"create_connection error: {e}"
        logging.error(msg=stderr)
        success = False
        conn = None
    finally:
        return success, stderr, conn


def create_dataset(conn: sqlite3.Connection, effort_data_dict: dict) -> (bool, str):
    logging.info(msg="Creating dataset")
    success: bool = False
    stderr: str = None
    try:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {__DB_TABLE_NAME__} VALUES (NULL, ?)", (str(effort_data_dict),))
        conn.commit()
        success = True
    except Error as e:
        stderr = f"create_dataset error: {e}"
        success = False
        logging.error(msg=stderr)
    finally:
        return success, stderr


def read_datasets(conn: sqlite3.Connection) -> (bool, list, str):
    logging.info(msg="Reading database..")
    success: bool = False
    datasets: list = []
    stderr: str = None
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {__DB_TABLE_NAME__}")
        datasets = cursor.fetchall()
        conn.commit()
        success = True
    except Error as e:
        success = False
        stderr = f"read_datasets error: {e}"
        logging.error(msg=stderr)
    finally:
        return success, datasets, stderr


def update_dataset(conn: sqlite3.Connection, effort_data_dict: dict, id: int) -> (bool, str):
    logging.info(msg="Updating database")
    try:
        cursor = conn.cursor()
        cursor.execute(f"REPLACE INTO {__DB_TABLE_NAME__} VALUES ({id}, ?)", (str(effort_data_dict),))
        conn.commit()
    except Error as e:
        stderr = f"update_dataset error: {e}"
        logging.error(msg=stderr)
        return False, str(e)


def delete_dataset(conn: sqlite3.Connection, id: int) -> (bool, str):
    logging.info(msg="Deleting database")
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {__DB_TABLE_NAME__} WHERE id=?", (id,))
        conn.commit()
    except Error as e:
        stderr = f"delete_dataset error: {e}"
        logging.error(msg=stderr)
        return False, str(e)


def _create_database(db_fp: str) -> (bool, str, sqlite3.Connection):
    logging.info(msg="Creating database")
    conn: sqlite3.connect = None
    success: bool = False
    stderr: str = ""
    if not exists(path=db_fp):
        file = open(db_fp, "w+")
        file.close()
    try:
        conn = sqlite3.connect(db_fp)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {__DB_TABLE_NAME__} (id INTEGER PRIMARY KEY,"
                       f"effort varchar(500) NOT NULL)")
    except Error as e:
        stderr = f"_create_database error: {e}"
        logging.error(msg=stderr)
        conn = None
        success = False
    finally:
        return success, stderr, conn


def close_connection(conn: sqlite3.Connection) -> (bool, str):
    try:
        conn.close()
        return True, "Connection closed."
    except (Error, AttributeError) as e:
        stderr = f"create_connection error: {e}"
        logging.error(msg=stderr)
        return False, e


def _database_exists(db_fp: str) -> bool:
    return exists(db_fp)


#: Main entry point - debugging
if __name__ == '__main__':
    path: str = os.getcwd() + "/database.db"
    conn_success, conn_err, db_conn = create_connection(db_fp=path)

    # Make fake data
    data_obj_1 = project_data.create_dataset(req_a_hours=1.5, des_hours=2.5, coding_hours=3.5, testing_hours=4.5,
                                             prjmgt_hours=5.5, effort_name="effort name here",
                                             effort_desc="description goes here",
                                             primary_key=1)
    data_json_str_1 = project_data.dataset_obj_to_json_str(dataset_obj=data_obj_1)

    json_dict_1 = project_data.dataset_json_str_to_dict(json_str=data_json_str_1)

    data_obj_2 = project_data.create_dataset(req_a_hours=6.5, des_hours=7.5, coding_hours=8.5, testing_hours=9.5,
                                             prjmgt_hours=10.5, effort_name="2effort name here",
                                             effort_desc="2description goes here",
                                             primary_key=2)
    data_json_str_2 = project_data.dataset_obj_to_json_str(dataset_obj=data_obj_2)

    json_dict_2 = project_data.dataset_json_str_to_dict(json_str=data_json_str_2)

    # Store data into database
    create_dataset(conn=db_conn, effort_data_dict=json_dict_1["effort"])
    create_dataset(conn=db_conn, effort_data_dict=json_dict_2["effort"])
    print(f"dict1 = {json_dict_1['effort']}\ndict2 = {json_dict_2['effort']}")

    # Update something in the database
    data_obj_3 = project_data.create_dataset(req_a_hours=0.0, des_hours=0.0, coding_hours=0.0, testing_hours=0.0,
                                             prjmgt_hours=0.0, effort_name="update example",
                                             effort_desc="update example",
                                             primary_key=2)
    data_json_str_3 = project_data.dataset_obj_to_json_str(dataset_obj=data_obj_3)

    json_dict_3 = project_data.dataset_json_str_to_dict(json_str=data_json_str_3)

    update_dataset(conn=db_conn, effort_data_dict=json_dict_3["effort"], id=5)

    # Delete something from the database
    delete_dataset(conn=db_conn, id=5)
    success, datasets, stderr = read_datasets(conn=db_conn)
    for dataset in datasets:
        print(dataset)
    #print(f"datasets read from db: \n{datasets}")

    close_connection(conn=db_conn)
