#: Imports
from src.shared.data import *
from django.http import HttpResponse
from src.database.db_manager import *



#: Functions
def user_create_datasets(request):
    # TODO - Get id of item(s) from request to create dataset(s)
    return ""


def user_read_datasets(request):
    db_succ, db_err, database_conn = create_connection(db_fp=DB_FILEPATH)
    is_success, get_datasets, get_stderr = read_datasets(conn=database_conn)
    return HttpResponse(get_datasets)


def user_update_datasets(request):
    # TODO - Get id of item(s) from request to update db
    return ""


def user_delete_datasets(request):
    # TODO - Get id of item(s) from request to delete dataset(s)
    return ""


