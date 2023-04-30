#: Imports
import os
import sys
from pathlib import Path
path = Path(os.path.dirname(os.path.realpath(__file__)))
parent_path = path.parent.absolute().parent.absolute()
parent_path_formatted = f"{parent_path}".replace('WindowsPath(','').replace('(','').replace(')','') + "\\" # type: ignore
sys.path.append(parent_path_formatted) # type: ignore
print(sys.path)
from shared.data import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from database.db_manager import *

from django.shortcuts import render
from django.views import generic
from . import models




# #: Classes
# class IndexView(generic.ListView):
#     context_object_name = 'presentations'
#     template_name = 'index.html'
    
#     def get_set(self):
#         return models.Presentation.objects.all()
    
# class DetailView(generic.DetailView):
#     context_object_name = 'presentation'
#     model = models.Presentation
#     template_name = 'detail.html'
    
# class CreateView(generic.CreateView):
#     model = models.Presentation
#     template_name = 'edit.html'
    
    



#: Functions
@csrf_exempt
def user_create_datasets(request) -> HttpResponse:
    data = json.loads(request.body)
    db = Database(database_filepath=DB_FILEPATH)
    prj = dataset_dict_to_obj(dict=data)
    success, status = db.create(project=prj)
    return HttpResponse(f"Success: {success}, Status: {status}")


def user_read_datasets(request) -> HttpResponse:
    db = Database(database_filepath=DB_FILEPATH)
    success, dataset_list, error = db.read()
    logging.info(f"Data read from the database: {dataset_list}")
    return HttpResponse(json.dumps(dataset_list))


@csrf_exempt
def user_update_datasets(request):
    db = Database(database_filepath=DB_FILEPATH)
    data = json.loads(request.body)
    print(f"data received = {data}")
    prj: Project = dataset_dict_to_obj(dict=data)
    success, status = db.update(project_id=prj.project_id,project=prj)
    return HttpResponse(f"Success: {success}, Status: {status}")


@csrf_exempt
def user_delete_dataset(request):
    db = Database(database_filepath=DB_FILEPATH)
    data = json.loads(request.body)
    print(f"data received = {data}")
    prj: Project = dataset_dict_to_obj(dict=data)
    success, status = db.delete(project_id=prj.project_id)
    return HttpResponse(f"Success: {success}, Status: {status}")


