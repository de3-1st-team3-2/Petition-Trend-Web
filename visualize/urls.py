from django.urls import path
from . import views
from .views import *

app_name = 'visualize'
urlpatterns = [
    path('chart/', views.epeople_chart, name="chart"),
    path('main/', views.main_chart, name="main")
]