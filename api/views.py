from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from api.serializers import ProblemListSerializer, ProblemDetailSerializer, SubmissionDetailSerializer
from problem.models import Problem
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from submission.models import Submission


class ProblemAPIListView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Problem.objects.all()
    serializer_class = ProblemListSerializer


class ProblemAPIDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer


class SubmissionAPIDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    queryset = Submission.objects.all()
    serializer_class = SubmissionDetailSerializer
