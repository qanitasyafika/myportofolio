import uuid
from django.db import models

class Experience(models.Model):
    CATEGORY_CHOICES = [
        ('organisasi', 'Organisasi'),
        ('kepanitiaan', 'Kepanitiaan'),
        ('pekerjaan', 'Pekerjaan'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='organisasi')
    ended_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_ongoing(self):
        return self.ended_at is None

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