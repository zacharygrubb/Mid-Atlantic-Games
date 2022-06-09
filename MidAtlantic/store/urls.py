import view as view
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
]