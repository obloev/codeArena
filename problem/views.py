from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from problem.forms import ProblemCreateForm
from problem.models import Problem
from django.urls import reverse


class ProblemView(DetailView):
    model = Problem
    context_object_name = 'problem'
    template_name = 'problem/problem.html'


@login_required
def problem_create_view(request):
    if request.user.is_superuser:
        form = ProblemCreateForm()
        if request.method == 'POST':
            form = ProblemCreateForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                data = request.POST
                indict = {}
                outdict = {}
                for i in range(1, 11):
                    indict[i] = data.get(f'in{i}')
                    outdict[i] = data.get(f'out{i}')
                p_data = {
                    "in": indict,
                    "out": outdict,
                }
                form.instance.data = p_data
                form.instance.author = request.user
                form.save()
                messages.success(request, 'Masala muvaffaqiyatli yaratildi')
                return redirect(reverse('problem:problem', args=[form.instance.id]))
        return render(request, 'problem/problem_create.html', {
            'form': form,
            'rang': range(1, 11),
        })
    raise Http404()


def all_problem(request):
    problems = Problem.objects.all()
    ac_problems = []
    attempts = []
    for problem in problems:
        try:
            ac_problem = problem.submission_set.filter(author=request.user, status_id=3).first()
            attempt = problem.submission_set.filter(author=request.user).first()
            if ac_problem:
                ac_problems.append(ac_problem.problem.id)
            if attempt:
                attempts.append(attempt.problem.id)
        except ValueError:
            pass
    return render(request, 'problem/all.html', {
        'problems': problems,
        'ac_attempts': ac_problems,
        'attempts': attempts,
    })
