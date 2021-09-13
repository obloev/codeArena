from django.urls import path
from accounts.views import all_users, SignUpView, profile


urlpatterns = [
    path('all/', all_users, name='all-users'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('<username>/', profile, name='profile'),
]
