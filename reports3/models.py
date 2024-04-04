from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location="media")

class Problem_cat_three(models.Model):
    image = models.ImageField(upload_to="reports/", storage=fs,)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="reported")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description
