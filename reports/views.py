# views.py
from rest_framework import generics
from .models import Problem
from .serializers import ProblemSerializer

class ProblemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer