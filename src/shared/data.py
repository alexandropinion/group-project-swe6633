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
# path = Path(os.path.dirname(os.path.realpath(__file__)))
# #path = Path(os.getcwd())
# parent_path = path.parent.absolute()
# parent_path_formatted = f"{parent_path}".replace('WindowsPath(','').replace('(','').replace(')','') + "\\" # type: ignore
# sys.path.append(parent_path_formatted) # type: ignore
# print(sys.path)
# from database import db_manager

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
    
    

    
    

class ReqAnalysis:
    def __init__(self, hours: float):
        self.hours = hours


class Design:
    def __init__(self, hours: float):
        self.hours = hours


class Coding:
    def __init__(self, hours: float):
        self.hours = hours


class Testing:
    def __init__(self, hours: float):
        self.hours = hours


class ProjectManagement:
    def __init__(self, hours: float):
        self.hours = hours


class Effort:
    def __init__(self, name: str, desc: str, req_a: ReqAnalysis, des: Design, code: Coding, test: Testing,
                 prjmgt: ProjectManagement):
        self.name = name
        self.desc = desc
        self.req_a = req_a
        self.des = des
        self.code = code
        self.test = test
        self.prjmgt = prjmgt


class Dataset:
    def __init__(self, dataset_id: int, effort: Effort):
        self.id = dataset_id
        self.effort = effort


class Encoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


#: Functions
def create_dataset(req_a_hours: float, des_hours: float, coding_hours: float, testing_hours: float,
                   prjmgt_hours: float, effort_name: str, effort_desc: str, primary_key: int) -> Dataset:
    req_a = ReqAnalysis(hours=req_a_hours)
    des = Design(hours=des_hours)
    coding = Coding(hours=coding_hours)
    testing = Testing(hours=testing_hours)
    prjmgt = ProjectManagement(hours=prjmgt_hours)
    effort = Effort(name=effort_name, desc=effort_desc, req_a=req_a, des=des, code=coding, test=testing,
                    prjmgt=prjmgt)

    return Dataset(dataset_id=primary_key, effort=effort)


def dataset_obj_to_json_str(dataset_obj: Dataset) -> str:
    return json.dumps(Encoder().encode(o=dataset_obj))


def dataset_json_str_to_dict(json_str: str) -> dict:
    return json.loads(json.loads(json_str))


def _get_all_dataset_keys() -> list:
    symbol_obj = create_dataset(req_a_hours=0.0, des_hours=0.0, coding_hours=0.0, testing_hours=0.0,
                                prjmgt_hours=0.0, effort_name="", effort_desc="", primary_key=0)
    symbol_json_str = dataset_obj_to_json_str(dataset_obj=symbol_obj)
    symbol_dict = dataset_json_str_to_dict(json_str=symbol_json_str)
    return [x for x in symbol_dict]

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