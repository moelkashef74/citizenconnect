# Python
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Problem

class ProblemModelTest(TestCase):
    def test_create_problem(self):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'\x00\x01\x02\x03', content_type='image/jpeg')
        problem = Problem.objects.create(
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