from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

fs = FileSystemStorage(location= settings.MEDIA_ROOT)
class Problem(models.Model):
    image = models.ImageField(upload_to="reports/", storage=fs,)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="reported")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description
