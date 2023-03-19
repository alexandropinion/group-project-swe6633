from django.shortcuts import render
from django.http import HttpResponse
from src.data import Dataset, Effort, ProjectManagement, Testing, Coding, Design, ReqAnalysis, Encoder
import json


def get_all_datasets(request):
    req_a = ReqAnalysis(hours=10.0)
    des = Design(hours=10.1)
    coding = Coding(hours=10.2)
    testing = Testing(hours=10.3)
    prjmgt = ProjectManagement(hours=10.4)
    effort = Effort(name="task 1", desc="this is a description", req_a=req_a, des=des, code=coding, test=testing,
                    prjmgt=prjmgt)
    dataset = Dataset(id=1, effort=effort)
    response = Encoder().encode(o=dataset)

    return HttpResponse(json.dumps(response))






