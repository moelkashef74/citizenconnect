# api/serializers.py
from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField(method_name='get_user_email')

    class Meta:
        model = Report
        fields = ['id','image', 'description', 'location', 'status', 'created_at','user']

        
    def get_user_email(self, obj):
        return obj.user.get_full_name