from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_datasets, name="get_all_datasets")
]