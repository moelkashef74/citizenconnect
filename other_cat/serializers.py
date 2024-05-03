# api/serializers.py
from rest_framework import serializers
from .models import Report_other

class ReportSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField(method_name='get_user_email')

    class Meta:
        model = Report_other
        fields = ['id','image', 'description', 'location', 'status', 'created_at','user', 'category']

        
    def get_user_email(self, obj):
        return obj.user.get_full_name