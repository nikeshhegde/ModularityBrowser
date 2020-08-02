from django import forms
from django.utils import timezone
# Create the form class.

LANGUAGE_CHOICES = [
    ('java', 'Java'),
    ('python', 'Python'),
]

class GitHubForm(forms.Form):
    project_url = forms.CharField(max_length=200)
    language_type = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    since_datetime = forms.CharField()
    until_datetime = forms.CharField()
