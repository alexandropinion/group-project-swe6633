from django.shortcuts import render
from django.http import HttpResponse
from src.data import Dataset, Effort, ProjectManagement, Testing, Coding, Design, ReqAnalysis, Encoder
import json



def create_data():
    return ""
def read_data(request):
    dataset = _create_temp_dataset()
    return HttpResponse(json.dumps(Encoder().encode(o=dataset)))

def update_data():
    return ""

def delete_data():
    return ""




def _create_temp_dataset() -> Dataset:
    req_a = ReqAnalysis(hours=10.0)
    des = Design(hours=10.1)
    coding = Coding(hours=10.2)
    testing = Testing(hours=10.3)
    prjmgt = ProjectManagement(hours=10.4)
    effort = Effort(name="task 1", desc="this is a description", req_a=req_a, des=des, code=coding, test=testing,
                    prjmgt=prjmgt)
    return Dataset(dataset_id=1, effort=effort)
