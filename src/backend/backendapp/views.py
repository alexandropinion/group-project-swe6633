from django.shortcuts import render
from django.http import HttpResponse

import src.data
from src.data import Dataset, Effort, ProjectManagement, Testing, Coding, Design, ReqAnalysis, Encoder
import json
from src.database.db_manager import *
from src.data import *


def user_create_datasets(request):
    return ""


def user_read_datasets(request):
    db_succ, db_err, database_conn = create_connection(db_fp=src.data.DB_FILEPATH)
    is_success, get_datasets, get_stderr = read_datasets(conn=database_conn)
    return HttpResponse(get_datasets)


def user_update_datasets(request):
    return ""


def user_delete_datasets(request):
    return ""


