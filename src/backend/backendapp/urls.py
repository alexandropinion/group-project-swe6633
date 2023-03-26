from django.urls import path
from . import views

urlpatterns = [
    path('', views.read_data, name="get_all_datasets")
]