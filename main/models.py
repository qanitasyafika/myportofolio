import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('organisasi', 'Organisasi'),
        ('kepanitiaan', 'Kepanitiaan'),
        ('magang', 'Magang'),
        ('riset', 'Riset'),
        ('lainnya', 'Lainnya'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='organisasi')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Project(models.Model):
    PROJECT_CHOICES = [
        ('research', 'Research Project'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('creative', 'Creative Arts'),
        ('organization', 'Organization Event'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=PROJECT_CHOICES, default='research')
    year = models.IntegerField()
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title