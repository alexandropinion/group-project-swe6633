import dataclasses
from json import JSONEncoder


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
    def __init__(self, id: int, effort: Effort):
        self.id = id
        self.effort = effort


class Encoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__
