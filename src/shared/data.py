#: Imports
from ast import List, Tuple
from dataclasses import dataclass
import dataclasses
import json
from json import JSONEncoder
import os
from pathlib import Path
from types import UnionType
from typing import List
from django import db
import sys

#: Globals
DB_FILEPATH = f"{Path(os.getcwd()).parent.absolute()}/group-project/src/database/database.db"


#: Classes
@dataclass 
class FuncReq:
    id: int
    project_id: int
    requirement: str
    owner:str
    
@dataclass 
class NonFuncReq:
    id: int
    project_id: int
    requirement: str
    owner:str
    
@dataclass
class Risks:
    id: int
    project_id: int
    risk: str
    risk_status: str
    
    
@dataclass
class Project:
    project_id: int
    project_name: str
    project_desc: str
    project_owner: str
    team_members: List[str]
    func_req: List[FuncReq]
    non_func_req: List[NonFuncReq]
    analysis_hours: float
    design_hours: float
    coding_hours: float
    testing_hours: float
    mgt_hours: float
    risks: List[Risks]
    

class Encoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


#: Functions
def dataset_json_str_to_dict(json_str: str) -> dict:
    return json.loads(json.loads(json_str))

def dataset_dict_to_obj(dict: dict) -> Project:
    func_req_list: list = []
    nonfunc_req_list: list = []
    risks_list: list = []
    project_list: list = []
    for req in dict["func_req"]:
        func_req_list.append(FuncReq(id=req["id"], project_id=req["project_id"], requirement=req["requirement"], owner=req["owner"]))
    for req in dict["non_func_req"]:
        nonfunc_req_list.append(NonFuncReq(id=req["id"], project_id=req["project_id"], requirement=req["requirement"], owner=req["owner"]))
    for risk in dict["risks"]:
        risks_list.append(Risks(id=risk["id"], project_id=risk["project_id"], risk=risk["risk"], risk_status=risk["risk_status"]))
    return Project(project_id=dict["project_id"], project_name=dict["project_name"], project_desc=dict["project_desc"], project_owner=dict["project_owner"], 
                   team_members=dict["team_members"], func_req=func_req_list, non_func_req=nonfunc_req_list, analysis_hours=dict["analysis_hours"],
                   design_hours=dict["design_hours"], coding_hours=dict["coding_hours"],
                   testing_hours=dict["testing_hours"], mgt_hours=dict["mgt_hours"], risks=risks_list) # type: ignore

def project_data_to_json(data: Project) -> str:
    return json.dumps(dataclasses.asdict(data))




#: Main entry point - debugging
if __name__ == '__main__':
    #: Example user input
    project_id = 4
    fq1 = FuncReq(id=1, project_id=project_id, requirement="this is a functional Bob requirement", owner="Bob")
    fq2 = FuncReq(id=2, project_id=project_id, requirement="this is a functional Sam requirement", owner="Sam")
    fq3 = FuncReq(id=3, project_id=project_id, requirement="this is a functional Jon requirement", owner="Jon")
    nfq1 = NonFuncReq(id=1, project_id=project_id, requirement="this is a non functional Bob requirement", owner="Bob")
    nfq2 = NonFuncReq(id=2, project_id=project_id, requirement="this is a non functional Bob requirement", owner="Bob")
    nfq3 = NonFuncReq(id=3, project_id=project_id, requirement="this is a non functional Bob requirement", owner="Bob")
    rsk1 = Risks(id=1, project_id=project_id, risk="this is a big risk", risk_status="Pending")
    rsk2 = Risks(id=1, project_id=project_id, risk="this is a small risk", risk_status="In-progress")
    prj = Project(project_id=project_id, project_name="Group 8 Project", project_desc="This is the best project.", project_owner="KSU", 
                  team_members=['Bob', 'Sam', 'Jon'], func_req=[fq1, fq2, fq3], non_func_req=[nfq1, nfq2, nfq3], analysis_hours=24.5, 
                  design_hours=13.2, coding_hours=45.5, testing_hours=16.5, mgt_hours=8.5, risks=[rsk1, rsk2])
    
    print(project_data_to_json(data=prj))
    # db = db_manager.DatabaseSingleton(database_filepath=DB_FILEPATH)
    # db.create(conn=db.conn, project=prj)
    # data = Project(id=None, func_req=['name: '])
    # data_obj = create_dataset(req_a_hours=1.5, des_hours=2.5, coding_hours=3.5, testing_hours=4.5,
    #                           prjmgt_hours=5.5, effort_name="effort name here", effort_desc="description goes here",
    #                           primary_key=1)
    # data_json_str = dataset_obj_to_json_str(dataset_obj=data_obj)

    # json_dict = dataset_json_str_to_dict(json_str=data_json_str)