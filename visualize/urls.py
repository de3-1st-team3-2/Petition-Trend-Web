from django.urls import path
from . import views
from .views import *

app_name = 'visualize'
urlpatterns = [
    path('cw24/', views.cw24_chart, name="CW24"),
]