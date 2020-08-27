from django import forms
from django.utils import timezone
# Create the form class.

DEPENDENCIES_TYPE = [
    ('File', 'File'),
    ('Class', 'Class'),
]

class GitHubForm(forms.Form):
    project_url = forms.CharField(max_length=200)
    dependencies_type = forms.ChoiceField(choices=DEPENDENCIES_TYPE)
