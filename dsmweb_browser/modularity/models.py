from django.db import models
from django.utils import timezone

# Create your models here.
class GitHub(models.Model):
    project_url = models.CharField(max_length=200)
    language_type = models.ChoiceField(choices=[('java', 'Java'), ('python', 'Python')])
    since_datetime = models.DateTimeField(blank=True, null=True)
    until_datetime = models.DateTimeField(default=timezone.now)
