#: Imports
from ast import Delete
import os
import sqlite3
import sys
from typing import List, Union
from pathlib import Path

import os

path = Path(os.path.dirname(os.path.realpath(__file__)))
parent_path = path.parent.absolute()
parent_path_formatted = f"{parent_path}".replace('WindowsPath(','').replace('(','').replace(')','') + "\\" # type: ignore
sys.path.append(parent_path_formatted) # type: ignore
from shared.data import DB_FILEPATH, FuncReq, NonFuncReq, Project, Risks, project_data_to_json 
from os.path import exists
from sqlite3 import Connection, Cursor, Error, connect
import logging

#: Globals
__DB_TABLE_NAME_PRJ__ = "project"
__DB_TABLE_NAME_FUNC__ = "funcreq"
__DB_TABLE_NAME_NON_FUNC__ = "nonfuncreq"
__DB_TABLE_NAME_RISKS__ = "risks"


#: Class
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class Database(metaclass=Singleton):
   
    def __init__(self, database_filepath: str) -> None:
        logging.info(msg="Instantiating database...")
        self.db_fp = database_filepath
        self.conn_success: bool
        self.conn_error: str
        self.conn: sqlite3.Connection
        self.connect(db_fp=database_filepath)  
        
        
    def connect(self, db_fp: str) -> None: # type: ignore
        logging.info(msg="Checking database setup...")
        success: bool = False
        stderr: str = ""
        conn: sqlite3.Connection = None # type: ignore
        if not exists(path=db_fp):
            file = open(db_fp, "w+")
            file.close()
        try:
            conn = sqlite3.connect(db_fp)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {__DB_TABLE_NAME_PRJ__} (project_id INTEGER PRIMARY KEY,"
                           f"project_name varchar(500) NOT NULL, project_desc varchar(500) NOT NULL, project_owner varchar(40) NOT NULL, " 
                           f"team_members varchar(100) NOT NULL, analysis_hours REAL NOT NULL, design_hours REAL NOT NULL, coding_hours REAL NOT NULL, "
                           f"testing_hours REAL NOT NULL, mgt_hours REAL NOT NULL)")
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {__DB_TABLE_NAME_FUNC__} (id INTEGER PRIMARY KEY,"
                           f"project_id INTEGER NOT NULL, requirement varchar(500) NOT NULL, owner varchar(40) NOT NULL)")
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {__DB_TABLE_NAME_NON_FUNC__} (id INTEGER PRIMARY KEY,"
                           f"project_id INTEGER NOT NULL, requirement varchar(500) NOT NULL, owner varchar(40) NOT NULL)")
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {__DB_TABLE_NAME_RISKS__} (id INTEGER PRIMARY KEY,"
                           f"project_id INTEGER NOT NULL, risk varchar(500) NOT NULL, risk_status varchar(40) NOT NULL)")
        except Error as e:
            stderr = f"_create_database error: {e}"
            logging.error(msg=stderr)
            conn = None # type: ignore
            success = False
        finally:
            self.conn_success = success
            self.conn_error = stderr
            self.conn = conn
        
   
    def create(self, project: Project) -> tuple[bool, str]:
        logging.info(msg="Creating project data...")
        success: bool = False
        stderr: str = None # type: ignore
        if not self.is_connected():
            print("CONNECTION DOWN...")
            logging.critical("Database connection is disconnected.")
            self.connect(db_fp=self.db_fp)
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {__DB_TABLE_NAME_PRJ__} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (project.project_name,project.project_desc, 
                                                                                                             project.project_owner, str(project.team_members), 
                                                                                                             project.analysis_hours, project.design_hours, 
                                                                                                             project.coding_hours, project.testing_hours, 
                                                                                                             project.mgt_hours,))
            for req in project.func_req:
                cursor.execute(f"INSERT INTO {__DB_TABLE_NAME_FUNC__} VALUES (NULL, ?, ?, ?)", (project.project_id,req.requirement, req.owner,))
            for req in project.non_func_req:
                cursor.execute(f"INSERT INTO {__DB_TABLE_NAME_NON_FUNC__} VALUES (NULL, ?, ?, ?)", (project.project_id,req.requirement, req.owner,))
            for risk in project.risks:
                cursor.execute(f"INSERT INTO {__DB_TABLE_NAME_RISKS__} VALUES (NULL, ?, ?, ?)", (project.project_id,risk.risk, risk.risk_status,))
            self.conn.commit()
            success = True
        except Error as e:
            stderr = f"Error creating data to put into the database.  Error: {e}"
            success = False
            logging.error(msg=stderr)
        finally:
            self.close()
            return success, stderr
    
    def read(self) -> tuple[bool, list, str]:
        logging.info(msg="Reading database..")
        if not self.is_connected():
            print("CONNECTION DOWN...")
            logging.critical("Database connection is disconnected.")
            self.connect(db_fp=self.db_fp)
        success: bool = False
        all_projects_json: List[str] = []
        stderr: str = None # type: ignore
        try:
            
            logging.info(msg="reading from the database")
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {__DB_TABLE_NAME_PRJ__}")
            prj_table = cursor.fetchall()
            cursor.execute(f"SELECT * FROM {__DB_TABLE_NAME_FUNC__}")
            func_table = cursor.fetchall()
            cursor.execute(f"SELECT * FROM {__DB_TABLE_NAME_NON_FUNC__}")
            nonfunc_table = cursor.fetchall()
            cursor.execute(f"SELECT * FROM {__DB_TABLE_NAME_RISKS__}")
            risk_table = cursor.fetchall()
            logging.info(msg=f"Data read from all tables:\n{prj_table}\n{func_table}\n{nonfunc_table}\n{risk_table}\n")
            all_risks: List[Risks] = [] # type: ignore
            all_func: List[FuncReq] = [] # type: ignore
            all_nonfunc: List[NonFuncReq] = [] # type: ignore
            all_projects: List[Project] = [] # type: ignore
            
                
            for risk in risk_table:
                print(f"risk: {risk}")
                all_risks.append(Risks(id=risk[0], project_id=risk[1], risk=risk[2], risk_status=risk[3]))
            for func in func_table:
                print(f"func: {func}")
                all_func.append(FuncReq(id=func[0], project_id=func[1], requirement=func[2], owner=func[3]))
            for nonfunc in nonfunc_table:
                all_nonfunc.append(NonFuncReq(id=nonfunc[0], project_id=nonfunc[1], requirement=nonfunc[2], owner=nonfunc[3]))
                print(f"nonfunc: {nonfunc}")
            for project in prj_table:
                all_projects.append(Project(project_id=project[0], project_name=project[1], project_desc=project[2], project_owner=project[3], 
                                            team_members=project[4], analysis_hours=project[5], design_hours=project[6], coding_hours=project[7], 
                                            testing_hours=project[8], mgt_hours=project[9], func_req=[x for x in all_func if x.project_id==project[0]], 
                                            non_func_req=[x for x in all_nonfunc if x.project_id==project[0]], risks=[x for x in all_risks if x.project_id==project[0]]))
            for each_project in all_projects:
                all_projects_json.append(project_data_to_json(data=each_project))
            success = True
        except (Error, Exception) as e:
            success = False
            stderr = f"Reading database error: {e}"
            logging.error(msg=stderr)
        finally:
            self.close()
            return success, all_projects_json, stderr
            
    
    def update(self, project_id: int, project: Project) -> tuple[bool, str]:
        success: bool = False
        status: str = ""
        logging.info(msg=f"Updating database for Project id {project_id}...")
        if not self.is_connected():
            logging.info("Reconnecting to the database...")
            self.connect(db_fp=self.db_fp)
        try:
            cursor: Cursor = self.conn.cursor()
            cursor.execute(f"REPLACE INTO {__DB_TABLE_NAME_PRJ__} VALUES ({project_id}, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           (project.project_name,project.project_desc, project.project_owner, str(project.team_members), project.analysis_hours,
                            project.design_hours, project.coding_hours, project.testing_hours, project.mgt_hours,))
            for req in project.func_req:
                cursor.execute(f"REPLACE INTO {__DB_TABLE_NAME_FUNC__} VALUES ({req.id}, ?, ?, ?)", (project.project_id,req.requirement, req.owner,))
            for req in project.non_func_req:
                cursor.execute(f"REPLACE INTO {__DB_TABLE_NAME_NON_FUNC__} VALUES ({req.id}, ?, ?, ?)", (project.project_id,req.requirement, req.owner,))
            for risk in project.risks:
                cursor.execute(f"REPLACE INTO {__DB_TABLE_NAME_RISKS__} VALUES ({risk.id}, ?, ?, ?)", (project.project_id,risk.risk, risk.risk_status,))
            self.conn.commit()
            success = True
            status = "Successfully updated the database."
        except Error as e:
            status = f"Error while attempting to update the database: {e}"
            logging.error(msg=status)
            success = False
            return False, str(e)
        finally:
            self.close()
            return success, status
    
    def delete(self, project_id: int) -> tuple[bool, str]: 
        success: bool = False
        status: str = ""
        logging.info(msg=f"Deleting database for Project id {project_id}...")
        if not self.is_connected():
            logging.info("Reconnecting to the database...")
            self.connect(db_fp=self.db_fp)
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {__DB_TABLE_NAME_PRJ__} WHERE project_id=?", (project_id,))
            cursor.execute(f"DELETE FROM {__DB_TABLE_NAME_FUNC__} WHERE project_id=?", (project_id,))
            cursor.execute(f"DELETE FROM {__DB_TABLE_NAME_NON_FUNC__} WHERE project_id=?", (project_id,))
            cursor.execute(f"DELETE FROM {__DB_TABLE_NAME_RISKS__} WHERE project_id=?", (project_id,))
            self.conn.commit()
            success = True
            status = f"Successfully deleted project id: {project_id}"
        except Error as e:
            stderr = f"delete_dataset error: {e}"
            logging.error(msg=stderr)
            success = False
        finally:
            return success, status
        
    def is_connected(self) -> bool:
        try:
            self.conn.cursor()
            return True
        except Exception:
            return False
        
    
    def close(self) -> None:
        try:
            self.conn.close()
        except:
            pass



def _database_exists(db_fp: str) -> bool:
    return exists(db_fp)


#: Main entry point - debugging
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    db = Database(database_filepath=DB_FILEPATH) # type: ignore
    #: Example user input
    project_id = 2
    db.delete(project_id=project_id)
    # fq1 = FuncReq(id=4, project_id=project_id, requirement="this is an updated functional requirement made by Maria", owner="Maria-Update") # type: ignore
    # fq2 = FuncReq(id=5, project_id=project_id, requirement="this is an updated functional requirement made by Dalton", owner="Dalton-Update") # type: ignore
    # fq3 = FuncReq(id=6, project_id=project_id, requirement="this is an updated functional requirement made by Wilbert", owner="Wilbert-Update") # type: ignore
    # nfq1 = NonFuncReq(id=4, project_id=project_id, requirement="this is an updated non functional requirement made by Tim.", owner="Tim-Update") # type: ignore
    # nfq2 = NonFuncReq(id=5, project_id=project_id, requirement="this is an updated non functional requirement made by Parker.", owner="Parker-Update") # type: ignore
    # nfq3 = NonFuncReq(id=6, project_id=project_id, requirement="this is an updated non functional requirement made by Betty.", owner="Betty-Update") # type: ignore
    # rsk1 = Risks(id=3, project_id=project_id, risk="This is an updated description of the risk", risk_status="This is the status of the risk.") # type: ignore
    # rsk2 = Risks(id=4, project_id=project_id, risk="This is an updated description of the risk", risk_status="In-progress") # type: ignore
    # prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best project.", project_owner="KSU", 
    #               team_members=['Bob', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=24.5, 
    #               design_hours=13.2, coding_hours=45.5, testing_hours=16.5, mgt_hours=8.5, risks=[rsk1, rsk2])
    
    # #print(project_data_to_json(data=prj))
    # db = Database(database_filepath=DB_FILEPATH) # type: ignore
    # #db.create(conn=db.conn, project=prj)
    # print(db.read())
    # print(db.update(project_id=2, project=prj))
    # db.close()
    
    
    # -- ORIGINAL DB SCHEMA/DEBUGGING
    #conn_success, conn_err, db_conn = create_connection(db_fp=project_data.DB_FILEPATH)
    #read_db_success, datasets, read_db_err =  read_datasets(conn=db_conn)

    #print(datasets)
    # path: str = os.getcwd() + "/database.db"
    # conn_success, conn_err, db_conn = create_connection(db_fp=path)
    #
    # # Make fake data
    # data_obj_1 = project_data.create_dataset(req_a_hours=1.5, des_hours=2.5, coding_hours=3.5, testing_hours=4.5,
    #                                          prjmgt_hours=5.5, effort_name="effort name here",
    #                                          effort_desc="description goes here",
    #                                          primary_key=1)
    # data_json_str_1 = project_data.dataset_obj_to_json_str(dataset_obj=data_obj_1)
    #
    # json_dict_1 = project_data.dataset_json_str_to_dict(json_str=data_json_str_1)
    #
    # data_obj_2 = project_data.create_dataset(req_a_hours=6.5, des_hours=7.5, coding_hours=8.5, testing_hours=9.5,
    #                                          prjmgt_hours=10.5, effort_name="2effort name here",
    #                                          effort_desc="2description goes here",
    #                                          primary_key=2)
    # data_json_str_2 = project_data.dataset_obj_to_json_str(dataset_obj=data_obj_2)
    #
    # json_dict_2 = project_data.dataset_json_str_to_dict(json_str=data_json_str_2)
    #
    # # Store data into database
    # create_dataset(conn=db_conn, effort_data_dict=json_dict_1["effort"])
    # create_dataset(conn=db_conn, effort_data_dict=json_dict_2["effort"])
    # print(f"dict1 = {json_dict_1['effort']}\ndict2 = {json_dict_2['effort']}")
    #
    # # Update something in the database
    # data_obj_3 = project_data.create_dataset(req_a_hours=0.0, des_hours=0.0, coding_hours=0.0, testing_hours=0.0,
    #                                          prjmgt_hours=0.0, effort_name="update example",
    #                                          effort_desc="update example",
    #                                          primary_key=2)
    # data_json_str_3 = project_data.dataset_obj_to_json_str(dataset_obj=data_obj_3)
    #
    # json_dict_3 = project_data.dataset_json_str_to_dict(json_str=data_json_str_3)
    #
    # update_dataset(conn=db_conn, effort_data_dict=json_dict_3["effort"], id=5)
    #
    # # Delete something from the database
    # delete_dataset(conn=db_conn, id=5)
    # success, datasets, stderr = read_datasets(conn=db_conn)
    # for dataset in datasets:
    #     print(dataset)
    # # print(f"datasets read from db: \n{datasets}")
    #
    # close_connection(conn=db_conn)
