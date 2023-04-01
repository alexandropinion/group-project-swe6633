#: Imports
from pathlib import Path
import pathlib
import sqlite3
import unittest
import os
import sys

from django import db
path = Path(os.path.dirname(os.path.realpath(__file__)))
parent_path = path.parent.absolute().parent.absolute()
parent_path_formatted = f"{parent_path}".replace('WindowsPath(','').replace('(','').replace(')','') + "\\" # type: ignore
sys.path.append(parent_path_formatted) # type: ignore
from db_manager import DB_FILEPATH, FuncReq, NonFuncReq, Project, Risks, project_data_to_json, Database, __DB_TABLE_NAME_FUNC__, __DB_TABLE_NAME_NON_FUNC__, __DB_TABLE_NAME_PRJ__, __DB_TABLE_NAME_RISKS__
import logging

#: Globals
__TEST_DB_FP__: str = f"{pathlib.Path(__file__).parent.resolve()}\\test_database.db"
__DB__ = Database(database_filepath=__TEST_DB_FP__) # type: ignore

#: Testcases
class TestUpdate(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        
        
    def test_create(self) -> None:
        logging.info("Starting test_create testcase...")
        logging.info(f"Setting up empty test database at {__TEST_DB_FP__} ...")
        if os.path.exists(__TEST_DB_FP__):
            self._prep_test_database()
            logging.info(f"Deleting {__TEST_DB_FP__}")
        __DB__.connect(db_fp=__TEST_DB_FP__)
        
        # Create data for the database
        logging.info("Creating test data to insert into the database...")
        project_id: int = 1  # Start with first project
        fq1 = FuncReq(id=1, project_id=project_id, requirement="this is a functional requirement made by Maria", owner="Maria") # type: ignore
        fq2 = FuncReq(id=2, project_id=project_id, requirement="this is a functional requirement made by Dalton", owner="Dalton") # type: ignore
        fq3 = FuncReq(id=3, project_id=project_id, requirement="this is a functional requirement made by Wilbert", owner="Wilbert") # type: ignore
        nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="this is a non functional requirement made by Tim.", owner="Tim") # type: ignore
        nfq2 = NonFuncReq(id=2, project_id=project_id, requirement="this is a non functional requirement made by Parker.", owner="Parker") # type: ignore
        nfq3 = NonFuncReq(id=3, project_id=project_id, requirement="this is a non functional requirement made by Betty.", owner="Betty") # type: ignore
        rsk1 = Risks(id=1, project_id=project_id, risk="This is a description of the risk", risk_status="This is the status of the risk.") # type: ignore
        rsk2 = Risks(id=2, project_id=project_id, risk="This is a description of the risk", risk_status="In-progress") # type: ignore
        prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best project.", project_owner="KSU", 
                    team_members=['Bob', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=24.5, 
                    design_hours=13.2, coding_hours=45.5, testing_hours=16.5, mgt_hours=8.5, risks=[rsk1, rsk2])
        success_prj, status_prj = __DB__.create(project=prj)
        logging.info(f"Reading data from test database...\nData read: \n{__DB__.read()}")
        #__DB__.conn.close()
        return self.assertEqual(success_prj, True)
    
    def test_update(self) -> None:
        logging.basicConfig(level=logging.INFO)
        # Setup the test database
        logging.info(f"Starting test_update testcase...\nSetting up empty test database at {__TEST_DB_FP__} ...")
        if os.path.exists(__TEST_DB_FP__):
            self._prep_test_database()
            logging.info(f"Deleting {__TEST_DB_FP__}")
        #db = Database(database_filepath=__TEST_DB_FP__) # type: ignore
        __DB__.connect(db_fp=__TEST_DB_FP__)
        
        # Create data for the database
        logging.info("Creating data into test database...")
        project_id: int = 1  # Start with first project
        fq1 = FuncReq(id=1, project_id=project_id, requirement="this is a functional requirement made by Maria", owner="Maria") # type: ignore
        fq2 = FuncReq(id=2, project_id=project_id, requirement="this is a functional requirement made by Dalton", owner="Dalton") # type: ignore
        fq3 = FuncReq(id=3, project_id=project_id, requirement="this is a functional requirement made by Wilbert", owner="Wilbert") # type: ignore
        nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="this is a non functional requirement made by Tim.", owner="Tim") # type: ignore
        nfq2 = NonFuncReq(id=2, project_id=project_id, requirement="this is a non functional requirement made by Parker.", owner="Parker") # type: ignore
        nfq3 = NonFuncReq(id=3, project_id=project_id, requirement="this is a non functional requirement made by Betty.", owner="Betty") # type: ignore
        rsk1 = Risks(id=1, project_id=project_id, risk="This is a description of the risk", risk_status="This is the status of the risk.") # type: ignore
        rsk2 = Risks(id=2, project_id=project_id, risk="This is a description of the risk", risk_status="In-progress") # type: ignore
        prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best project.", project_owner="KSU", 
                    team_members=['Bob', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=24.5, 
                    design_hours=13.2, coding_hours=45.5, testing_hours=16.5, mgt_hours=8.5, risks=[rsk1, rsk2])
        success_prj, status_prj = __DB__.create(project=prj)
        
        read_succ, read_list, read_err = __DB__.read()
        print(f"data read from database: {read_list}")
        logging.info(f"Reading data from test database...\nData read: \n{read_list}")
        logging.info(f"Updating database with new test data...")
        fq1 = FuncReq(id=1, project_id=project_id, requirement="this is an updated functional requirement made by Maria", owner="Maria-Update") # type: ignore
        fq2 = FuncReq(id=2, project_id=project_id, requirement="this is an updated functional requirement made by Dalton", owner="Dalton-Update") # type: ignore
        fq3 = FuncReq(id=3, project_id=project_id, requirement="this is an updated functional requirement made by Wilbert", owner="Wilbert-Update") # type: ignore
        nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="this is an updated non functional requirement made by Tim.", owner="Tim-Update") # type: ignore
        nfq2 = NonFuncReq(id=2, project_id=project_id, requirement="this is an updated non functional requirement made by Parker.", owner="Parker-Update") # type: ignore
        nfq3 = NonFuncReq(id=3, project_id=project_id, requirement="this is an updated non functional requirement made by Betty.", owner="Betty-Update") # type: ignore
        rsk1 = Risks(id=1, project_id=project_id, risk="This is an updated description of the risk", risk_status="This is the status of the risk.") # type: ignore
        rsk2 = Risks(id=2, project_id=project_id, risk="This is an updated description of the risk", risk_status="In-progress") # type: ignore
        updated_prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best project.", project_owner="KSU-Updated", 
                    team_members=['Bob-Updated', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=0.5, 
                    design_hours=0.2, coding_hours=0.5, testing_hours=0.5, mgt_hours=0.5, risks=[rsk1, rsk2])
        
        success_updated_prj, status_updated_prj = __DB__.update(project_id=project_id, project=updated_prj)
        logging.info(f"Updated project data complete. Status: {status_updated_prj}, Success: {success_updated_prj}")
        print("test complete")
        return self.assertEqual(success_updated_prj, success_prj)
    
    def test_delete(self):
        logging.basicConfig(level=logging.INFO)
        # Setup the test database
        logging.info(f"Starting test_delete testcase...\nSetting up empty test database at {__TEST_DB_FP__} ...")
        if os.path.exists(__TEST_DB_FP__):
            self._prep_test_database()
            logging.info(f"Deleting {__TEST_DB_FP__}")
        __DB__.connect(db_fp=__TEST_DB_FP__)
        
        #: Create data
        logging.info("Creating data into test database...")
        project_id: int = 1  # Start with first project
        fq1 = FuncReq(id=1, project_id=project_id, requirement="this is a functional requirement made by Maria", owner="Maria") # type: ignore
        fq2 = FuncReq(id=2, project_id=project_id, requirement="this is a functional requirement made by Dalton", owner="Dalton") # type: ignore
        fq3 = FuncReq(id=3, project_id=project_id, requirement="this is a functional requirement made by Wilbert", owner="Wilbert") # type: ignore
        nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="this is a non functional requirement made by Tim.", owner="Tim") # type: ignore
        nfq2 = NonFuncReq(id=2, project_id=project_id, requirement="this is a non functional requirement made by Parker.", owner="Parker") # type: ignore
        nfq3 = NonFuncReq(id=3, project_id=project_id, requirement="this is a non functional requirement made by Betty.", owner="Betty") # type: ignore
        rsk1 = Risks(id=1, project_id=project_id, risk="This is a description of the risk", risk_status="This is the status of the risk.") # type: ignore
        rsk2 = Risks(id=2, project_id=project_id, risk="This is a description of the risk", risk_status="In-progress") # type: ignore
        prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best project.", project_owner="KSU", 
                    team_members=['Bob', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=24.5, 
                    design_hours=13.2, coding_hours=45.5, testing_hours=16.5, mgt_hours=8.5, risks=[rsk1, rsk2])
        success_create, status_create = __DB__.create(project=prj)
        
        
        #: Example user input
        __DB__.connect(db_fp=__TEST_DB_FP__)
        delete_project_id = 1
        success_delete, status_delete = __DB__.delete(project_id=delete_project_id)
        return self.assertEqual(success_delete, success_create)
    
        
    
    def _prep_test_database(self) -> None:
        logging.info("Preparing the test database...")
        __DB__.connect(db_fp=__TEST_DB_FP__)
        cursor: sqlite3.Cursor = __DB__.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #conn.commit()
        tables = cursor.fetchall()
        logging.info(f"All tables discovered while preparing the test database: {tables}")
        
        cursor.execute(f"DROP table IF EXISTS {__DB_TABLE_NAME_RISKS__};")
        cursor.execute(f"DROP table IF EXISTS {__DB_TABLE_NAME_PRJ__};")
        cursor.execute(f"DROP table IF EXISTS {__DB_TABLE_NAME_FUNC__};")
        cursor.execute(f"DROP table IF EXISTS {__DB_TABLE_NAME_NON_FUNC__};")
        __DB__.conn.commit()
        __DB__.close()
            
    
# class TestCreate(unittest.TestCase):
#     def __init__(self, methodName: str = "runTest") -> None:
#         super().__init__(methodName)
#         logging.basicConfig(level=logging.INFO)
        
#     def test_create(self) -> None:
#         logging.info("Starting test_create testcase...")
#         logging.info(f"Setting up empty test database at {__TEST_DB_FP__} ...")
#         if os.path.exists(__TEST_DB_FP__):
#             logging.info(f"Deleting {__TEST_DB_FP__}")
#             os.remove(__TEST_DB_FP__)
#         #db = Database(database_filepath=__TEST_DB_FP__) # type: ignore
        
#         # Create data for the database
#         logging.info("Creating test data to insert into the database...")
#         project_id: int = 1  # Start with first project
#         fq1 = FuncReq(id=1, project_id=project_id, requirement="this is a functional requirement made by Maria", owner="Maria") # type: ignore
#         fq2 = FuncReq(id=2, project_id=project_id, requirement="this is a functional requirement made by Dalton", owner="Dalton") # type: ignore
#         fq3 = FuncReq(id=3, project_id=project_id, requirement="this is a functional requirement made by Wilbert", owner="Wilbert") # type: ignore
#         nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="this is a non functional requirement made by Tim.", owner="Tim") # type: ignore
#         nfq2 = NonFuncReq(id=2, project_id=project_id, requirement="this is a non functional requirement made by Parker.", owner="Parker") # type: ignore
#         nfq3 = NonFuncReq(id=3, project_id=project_id, requirement="this is a non functional requirement made by Betty.", owner="Betty") # type: ignore
#         rsk1 = Risks(id=1, project_id=project_id, risk="This is a description of the risk", risk_status="This is the status of the risk.") # type: ignore
#         rsk2 = Risks(id=2, project_id=project_id, risk="This is a description of the risk", risk_status="In-progress") # type: ignore
#         prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best project.", project_owner="KSU", 
#                     team_members=['Bob', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=24.5, 
#                     design_hours=13.2, coding_hours=45.5, testing_hours=16.5, mgt_hours=8.5, risks=[rsk1, rsk2])
#         success_prj, status_prj = __DB__.create(project=prj)
#         logging.info(f"Reading data from test database...\nData read: \n{__DB__.read()}")
#         #__DB__.conn.close()
#         return self.assertEqual(success_prj, True)
    
    
# def suite() -> unittest.TestSuite:
#       suite = unittest.TestSuite()
#       suite.addTest(TestCreate('test_create'))
#       suite.addTest(TestUpdate('test_update'))
      
#       return suite
        
        
#: Run unit tests        
if __name__ == '__main__':
    #unittest.main()
    # runner = unittest.TextTestRunner(failfast=True)
    # runner.run(suite())
    logging.basicConfig(level=logging.INFO)
    test_order: list[str] = ["test_create", "test_update"] # could be sys.argv
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
    unittest.main(testLoader=loader, verbosity=2)