from django.forms import ModelForm
from problem.models import Problem


class ProblemCreateForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'desc', 'level', 'input_info', 'output_info']
