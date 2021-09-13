from django.urls import path
from api.views import ProblemAPIListView, ProblemAPIDetailView, SubmissionAPIDetailView

app_name = 'api'

urlpatterns = [
    path('problems/', ProblemAPIListView.as_view(), name='problem_list_api'),
    path('problems/<id>/', ProblemAPIDetailView.as_view(), name='problem_detail_api'),
    path('submission/<id>/', SubmissionAPIDetailView.as_view(), name="submission_detail_api"),
]
