import uuid
from django.contrib.auth.models import User
from django.db import models

class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    starred_by = models.ManyToManyField(
        User, related_name="starred_experiences", blank=True
    )

    def __str__(self):
        return self.title


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True, default='')
    project_image_url = models.URLField(blank=True, default='')
    starred_by = models.ManyToManyField(User, related_name='starred_projects', blank=True)

    def __str__(self):
        return self.title