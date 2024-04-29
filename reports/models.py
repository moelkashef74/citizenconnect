
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import random
import string
from accounts.models import User

fs = FileSystemStorage(location= settings.MEDIA_ROOT)


class Report(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    image = models.ImageField(upload_to="reports/", storage=fs,)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="reported")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")


    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                if not Report.objects.filter(id=random_id).exists():
                    self.id = random_id
                    break
        super().save(*args, **kwargs)
