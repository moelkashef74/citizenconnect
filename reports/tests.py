# Python
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Report
from .utils import geocode_location
from unittest.mock import patch

class ProblemModelTest(TestCase):
    def test_create_problem(self):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'\x00\x01\x02\x03', content_type='image/jpeg')
        problem = Report.objects.create(
            category='Traffic Light',
            image=image,
            description='A broken traffic light at the intersection.',
            location='123 Main St',
            status='reported'
        )
        self.assertEqual(problem.category, 'Traffic Light')
        self.assertEqual(problem.description, 'A broken traffic light at the intersection.')
        self.assertEqual(problem.location, '123 Main St')
        self.assertEqual(problem.status, 'reported')

class GeocodingTestCase(TestCase):
    @patch('your_app.utils.Nominatim')
    def test_geocode_location(self, mock_geolocator):
        # Mock the geolocator's reverse method
        mock_geolocator.return_value.reverse.return_value.address = '123 Main St'

        # Call the geocode_location function with test coordinates
        address = geocode_location(40.7128, -74.0060)