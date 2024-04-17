from django.urls import path
from . import views
from .views import *

app_name = 'visualize'
urlpatterns = [
    path('epeople/', epeople_chart),
    path('congress/', congress_chart),
    path('cw24/', cw24_chart),
    path('ideaseoul/', ideaseoul_chart),
]