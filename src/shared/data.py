#: Imports
import json
from json import JSONEncoder
import os
from pathlib import Path

#: Globals
DB_FILEPATH = f"{Path(os.getcwd()).parent.absolute()}/database/database.db"


#: Classes
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


#: Main entry point - debugging
if __name__ == '__main__':
    data_obj = create_dataset(req_a_hours=1.5, des_hours=2.5, coding_hours=3.5, testing_hours=4.5,
                              prjmgt_hours=5.5, effort_name="effort name here", effort_desc="description goes here",
                              primary_key=1)
    data_json_str = dataset_obj_to_json_str(dataset_obj=data_obj)

    json_dict = dataset_json_str_to_dict(json_str=data_json_str)