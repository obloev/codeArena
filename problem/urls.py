from django.urls import path
from problem.views import *

app_name = 'problem'

urlpatterns = [
    path('', all_problem, name='all'),
    path('create/', problem_create_view, name='create'),
    path('<pk>/', ProblemView.as_view(), name='problem'),
]
