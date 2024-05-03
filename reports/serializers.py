from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user_email')
    other = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Report
        fields = ['id', 'image', 'description', 'location', 'status', 'created_at', 'user', 'category', 'other']
        extra_kwargs = {
            'category': {
                'required': True,
                'allow_blank': False,
            }
        }

    def get_user_email(self, obj):
        return obj.user.get_full_name

    def validate(self, data):
        category = data.get('category')
        other = data.get('other')

        if category == 'other' and not other:
            raise serializers.ValidationError({
                'other': 'This field is required when "Other" is selected as category.'
            })
        return data

    def create(self, validated_data):
        if validated_data.get('category') == 'other':
            validated_data['category'] = validated_data.pop('other')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('category') == 'other':
            instance.category = validated_data.pop('other')
        return super().update(instance, validated_data)
