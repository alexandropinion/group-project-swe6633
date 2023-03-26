from django.urls import path
from . import views

urlpatterns = [
    path('user-create-datasets', views.user_create_datasets, name="user_create_datasets"),
    path('user-read-datasets', views.user_read_datasets, name="user_read_datasets"),
    path('user-update-datasets', views.user_update_datasets, name="user_update_datasets"),
    path('user-delete-datasets', views.user_delete_datasets, name="user_delete_datasets")
]
