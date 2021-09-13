from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import User
from problem.models import Problem
from submission.models import Submission


def profile(request, username):
    user = get_object_or_404(User, username=username)
    ac_submissions = Submission.objects.filter(
        author=user,
        status_id=3,
    )
    users = User.objects.order_by('-score').all()
    rating = [user for user in users]
    rate = rating.index(user) + 1
    submissions = Submission.objects.filter(author=user)
    ac_problems = list(set([submission.problem.id for submission in ac_submissions]))
    return render(request, 'registration/profile.html', {
        'user': user,
        'ac_p': ac_problems[::-1],
        'submissions': submissions[:10],
        's_count': submissions.count(),
        'rate': rate,
    })


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def home_view(request):
    problems = Problem.objects.count()
    submissions = Submission.objects.count()
    users = User.objects.count()
    leader_board = User.objects.order_by('-score')[:3]
    top3_pr = [
        [
            problem.submission_set.count(),
            problem.id,
            problem.title,
        ]
        for problem in Problem.objects.all()
    ]
    top3_pr.sort()
    top3_pr = top3_pr[::-1][:3]
    return render(request, 'home.html', {
        'pr_c': problems,
        'sb_c': submissions,
        'us_c': users,
        'lb': leader_board,
        'top_3_pr': top3_pr,
    })


def all_users(request):
    users = User.objects.order_by('-score').all()
    return render(request, 'all_users.html', {
        'users': users,
    })
