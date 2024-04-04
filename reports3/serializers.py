# api/serializers.py
from rest_framework import serializers
from .models import Problem_cat_three


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem_cat_three
        fields = ['image', 'description', 'location', 'status', 'created_at']