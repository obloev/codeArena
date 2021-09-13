import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from submission.models import Submission
from django.shortcuts import get_object_or_404, redirect, render
from problem.models import Problem
import base64
import json


def base64decode(value):
    if value is None:
        return None
    enc = value.encode('ascii')
    dec = base64.b64decode(enc).decode('ascii')
    return dec


def any_no_result(response):
    return any([i['status']['id'] in [1, 2] for i in response.json()['submissions']])


url = "https://judge0-ce.p.rapidapi.com/submissions/batch"

headers = {
    'content-type': "application/json",
    'x-rapidapi-key': "3fdd7f0747msh5f8800058098df9p1ee141jsn40c42d3053c5",
    # 'x-rapidapi-key': "a7fc2d2151msh17a97176068c096p117356jsnf4b2d02d0adb",
    'x-rapidapi-host': "judge0-ce.p.rapidapi.com"
}


def run(lang_id, code, problem):
    querystring = {
        "base64_encoded": "false"
    }

    submissions = []
    for i in range(1, 11):
        submissions.append({
            "language_id": lang_id,
            "source_code": code,
            "expected_output": problem.data['out'][str(i)],
            "stdin": problem.data['in'][str(i)],
            "memory-limt": 1024,
            "cpu_time_limit": 1,
        })

    payload = json.dumps({
        "submissions": submissions
    }, indent=4)

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        params=querystring
    )

    print(response)

    querystring = {
        "tokens": ",".join([i['token'] for i in response.json()]),
        "base64_encoded": "true",
        "wait": "false",
        "fields": ",".join([
            'source_code',
            'stdin',
            'expected_output',
            'stdout',
            'created_at',
            'finished_at',
            'time',
            'memory',
            'stderr',
            'token',
            'exit_code',
            'status',
            'language'
        ])
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=querystring
    )

    if any_no_result(response):
        while any_no_result(response):
            response = requests.request(
                "GET",
                url,
                headers=headers,
                params=querystring
            )

    return response.json()['submissions']


@login_required
def create_submission(request):
    if request.method == 'POST':
        data = request.POST
        problem = get_object_or_404(Problem, id=data['problem_id'])
        code = data['code']
        lang_id = data['lang']
        try:
            results = run(lang_id, code, problem)
            status = ''
            lang = results[0]['language']['name']
            time = [0]
            memory = [0]
            status_id = 0

            for result in results:
                print(result['stdout'])
                memory.append(int(result['memory']) if result['memory'] is not None else 0)
                time.append(float(result['time']) if result['time'] is not None else 0)
                if result['stdout'] is None and result['status']['id'] == 4:
                    status = 'No Output'
                    status_id = 15
                    break
                elif result['status']['id'] != 3:
                    status = result['status']['description']
                    status_id = result['status']['id']
                    break
                else:
                    status = result['status']['description']
                    status_id = result['status']['id']

            submission = Submission(
                problem=problem,
                author=request.user,
                status=status,
                language=lang,
                memory=round(max(memory) / 1024),
                time=round(max(time) * 1000),
                code=code,
                lang_id=lang_id,
                status_id=status_id,
            )

            submission.save()
            ac_submission = Submission.objects.filter(
                author=submission.author,
                status_id=3,
                problem=problem,
            )
            if submission.status_id == 3 and ac_submission.count() < 2:
                author = submission.author
                if submission.problem.level == 'Oson':
                    author.score += 3
                elif submission.problem.level == 'Murakkab':
                    author.score += 7
                else:
                    author.score += 5
                author.save()
            return redirect(submission.get_absolute_url())

        except ValueError:
            messages.error(request, "Kod bo'sh yoki serverda xato")
            return redirect(reverse('problem:problem', args=[problem.id]))


def get_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if request.user == submission.author:
        return render(request, 'submission/main.html', {
            'submission': submission,
        })
    return redirect(reverse('attempt:all'))


def all_submissions(request):
    submissions = Submission.objects.all()
    return render(request, 'submission/all.html', {
        'submissions': submissions,
    })
