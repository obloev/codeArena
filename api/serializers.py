from rest_framework import serializers
from problem.models import Problem
from submission.models import Submission


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'title', 'url']


class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'title', 'desc', 'input_info', 'output_info', 'level', 'inputs', 'outputs']


class SubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
