from django.urls import path
from . import views
#import views

urlpatterns = [
    path('user-create-datasets', views.user_create_datasets, name="user_create_datasets"),  # type: ignore
    path('user-read-datasets', views.user_read_datasets, name="user_read_datasets"),
    path('user-update-datasets', views.user_update_datasets, name="user_update_datasets"), # type: ignore
    path('user-delete-dataset', views.user_delete_dataset, name="user_delete_dataset") # type: ignore
]