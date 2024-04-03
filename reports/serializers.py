# api/serializers.py
from rest_framework import serializers
from .models import Problem
from .models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['image', 'description', 'location', 'status', 'created_at']