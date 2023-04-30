import sys
from django.test import TestCase
from pathlib import Path

import os

path = Path(os.path.dirname(os.path.realpath(__file__)))
parent_path = path.parent.absolute().parent.absolute()
parent_path_formatted = f"{parent_path}".replace('WindowsPath(','').replace('(','').replace(')','') + "\\" # type: ignore
sys.path.append(parent_path_formatted) # type: ignore
import requests
from shared.data import *


def test_user_create_datasets() -> requests.Response:
    # Create project data
    project_id = 0
    fq1 = FuncReq(id=1, project_id=project_id, requirement="this is POST request test", owner="Post")
    fq2 = FuncReq(id=2, project_id=project_id, requirement="this is POST request test", owner="Penny")
    fq3 = FuncReq(id=3, project_id=project_id, requirement="this is POST request test", owner="Peter")
    nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="this is POST request test2", owner="Post")
    nfq2 = NonFuncReq(id=2, project_id=project_id, requirement="this is POST request test2", owner="Penny")
    nfq3 = NonFuncReq(id=3, project_id=project_id, requirement="this is POST request test2", owner="Peter")
    rsk1 = Risks(id=1, project_id=project_id, risk="this is a big risk", risk_status="Pending")
    rsk2 = Risks(id=1, project_id=project_id, risk="this is a small risk", risk_status="In-progress")
    prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best POST project.", project_owner="KSU-POST", 
                  team_members=['Bob', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=24.5, 
                  design_hours=13.2, coding_hours=45.5, testing_hours=16.5, mgt_hours=8.5, risks=[rsk1, rsk2])
    postdata = project_data_to_json(data=prj)
    return requests.post('http://127.0.0.1:8000/user-create-datasets', data=postdata)

def test_user_read_datasets() -> None:
    data = requests.get('http://127.0.0.1:8000/user-read-datasets')
    print(data.content)
    
def test_user_update_datasets() -> requests.Response:
    project_id = 3  # Ensure this project id exists within the database in order for it to be updated.
    fq1 = FuncReq(id=1, project_id=project_id, requirement="this is POST request test to UPDATE a dataset", owner="Post-UPDATE")
    fq2 = FuncReq(id=2, project_id=project_id, requirement="this is POST request test to UPDATE", owner="Penny-UPDATE")
    fq3 = FuncReq(id=3, project_id=project_id, requirement="this is POST request test to UPDATE", owner="Peter-UPDATE")
    nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="this is POST request test2", owner="Post-UPDATE")
    nfq2 = NonFuncReq(id=2, project_id=project_id, requirement="this is POST request test2", owner="Penny-UPDATE")
    nfq3 = NonFuncReq(id=3, project_id=project_id, requirement="this is POST request test2", owner="Peter-UPDATE")
    rsk1 = Risks(id=1, project_id=project_id, risk="this is a big risk", risk_status="Pending-UPDATE")
    rsk2 = Risks(id=1, project_id=project_id, risk="this is a small risk", risk_status="In-progress-UPDATE")
    prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best POST project.", project_owner="KSU-POST-UPDATE", 
                  team_members=['Bob', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=14.5, 
                  design_hours=1.2, coding_hours=1.5, testing_hours=1.5, mgt_hours=1.5, risks=[rsk1, rsk2])
    postdata = project_data_to_json(data=prj)
    return requests.post('http://127.0.0.1:8000/user-update-datasets', data=postdata)

def test_user_delete_dataset(project_id_to_delete: int):
    project_id = 4  # Ensure this project id exists within the database in order for it to be updated.
    fq1 = FuncReq(id=1, project_id=project_id, requirement="", owner="")
    nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="", owner="")
    rsk1 = Risks(id=1, project_id=project_id, risk="", risk_status="")
    prj = Project(project_id=project_id, project_name="", project_desc="", project_owner="", 
                  team_members=[''], func_req=[fq1], non_func_req=[nfq1], analysis_hours=0.0, 
                  design_hours=1.2, coding_hours=1.5, testing_hours=1.5, mgt_hours=1.5, risks=[rsk1])
    postdata = project_data_to_json(data=prj)
    return requests.post('http://127.0.0.1:8000/user-delete-dataset', data=postdata)



# Create your tests here.

#: Main entry point - debugging
if __name__ == '__main__':
    input("Press enter to create dataset...")
    test_user_create_datasets()
    input("Press enter to read dataset...")
    test_user_read_datasets()
    input("Press enter to update dataset...")
    test_user_update_datasets()
    input("press enter to update dataset...")
    test_user_delete_dataset(project_id_to_delete=int(input("Enter project id to delete: ")))