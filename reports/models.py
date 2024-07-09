
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import random
import string
from accounts.models import User
from django.db.models import JSONField
from django.core.files.storage import default_storage
from django.utils.encoding import smart_str



class Report(models.Model):
    CATEGORY_CHOICES = [
        ('Environmental', 'env'),
        ('Road', 'road'),
        ('Electric', 'elec'),
        ('other', 'Other'),
    ]

    id = models.CharField(primary_key=True, max_length=10, editable=False)
    image = models.ImageField(upload_to="reports/")
    description = models.TextField()
    location = models.TextField()
    status = models.CharField(max_length=20, default="reported")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    category = models.CharField( max_length=20, choices=CATEGORY_CHOICES )
    notification = JSONField(blank=True, null=True)

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
