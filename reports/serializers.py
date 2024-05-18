from rest_framework import serializers
from .models import Report
from accounts.models import User
from .utils import geocode_location
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name']  # Add other fields you want to display

class UserFieldSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name        

class ReportSerializer(serializers.ModelSerializer):
    user = UserFieldSerializer(read_only=True)
    other = serializers.CharField(write_only=True, required=False)
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    location = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Report
        fields = ['id', 'image', 'description', 'location', 'status', 'created_at', 'user', 'category', 'other', 'latitude', 'longitude']
        extra_kwargs = {
            'category': {
                'required': True,
                'allow_blank': False,
            }
        }

    def get_user_phone(self, obj):
        return obj.user.phone

    def validate(self, data):
        category = data.get('category')
        other = data.get('other')

        if category == 'other' and not other:
            raise serializers.ValidationError({
                'other': 'This field is required when "Other" is selected as category.'
            })

        latitude = data.get('latitude')
        longitude = data.get('longitude')
        location = data.get('location')

        if not location and latitude is not None and longitude is not None:
            # Perform geocoding to fill in the location
            data['location'] = geocode_location(latitude, longitude)
        elif not location:
            raise serializers.ValidationError({'location': 'This field may not be blank if latitude and longitude are not provided.'})


        return data

    def create(self, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)

        # Only attempt geocoding if both latitude and longitude are provided
        if latitude is not None and longitude is not None:
            try:
                address = geocode_location(latitude, longitude)
                if address:
                    validated_data['location'] = address
                else:
                    raise serializers.ValidationError({'location': 'Geocoding failed to return an address.'})
            except Exception as e:  # Replace with specific exceptions you expect from geocode_location
                raise serializers.ValidationError({'location': str(e)})
        elif not validated_data.get('location'):
            # If location is not provided and geocoding is not possible, raise an error
            raise serializers.ValidationError({'location': 'This field is required.'}) 

        if validated_data.get('category') == 'other':
            validated_data['category'] = validated_data.pop('other')

        return super().create(validated_data)