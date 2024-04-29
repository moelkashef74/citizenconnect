# api/serializers.py
from rest_framework import serializers
from .models import Report_cat_three


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report_cat_three
        fields = ['id','image', 'description', 'location', 'status', 'created_at']