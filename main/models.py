import uuid
from django.db import models

class Experience(models.Model):
    CATEGORY_CHOICES = [
        ('organisasi', 'Organisasi'),
        ('kepanitiaan', 'Kepanitiaan'),
        ('pekerjaan', 'Pekerjaan'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='organisasi')
    is_ongoing = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True, default='')
    project_image_url = models.URLField(blank=True, default='')

    def __str__(self):
        return self.title