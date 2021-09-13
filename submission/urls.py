from django.urls import path
from submission.views import create_submission, all_submissions, get_submission

app_name = 'attempt'

urlpatterns = [
    path('create/', create_submission, name='create'),
    path('', all_submissions, name='all'),
    path('<pk>', get_submission, name='get'),
]
