from django.urls import path
from . import views
from .views import *

app_name = 'visualize'
urlpatterns = [
    path('epeople/', epeople_chart),
    path('congress/', congress_chart),
    path('cw24/', cw24_chart),
    path('ideaseoul/', ideaseoul_chart),
    path('subthink/', subthink_chart),
    path('search/', search_main),
    path('search/result/', search_result),
    path('generate_wordcloud/<str:site>/', generate_wordcloud, name='generate_wordcloud'),
]