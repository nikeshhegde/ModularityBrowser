import os
with os.add_dll_directory("D:\\UCC Semesters\\Thesis\\Softwares\\SciTools\\bin\\pc-win64"):
    import understand
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import GitHubForm
from .main import start
from .UnderstandService import create_udb,execute

# Create your views here.
def index(request):

    if request.method=='POST':
        form = GitHubForm(request.POST)
        if form.is_valid():
            project_url = form.cleaned_data['project_url']
            language_type = form.cleaned_data['language_type']
            since_datetime = form.cleaned_data['since_datetime']
            until_datetime = form.cleaned_data['until_datetime']

            context = {
            'project_url': project_url,
            'language_type': language_type,
            'since_datetime': since_datetime,
            'until_datetime': until_datetime
            }

            start(project_url,language_type,since_datetime,until_datetime)

            template = loader.get_template('modularity/github_data.html')

            return HttpResponse(template.render(context, request))

    else:
        form = GitHubForm()
    return render(request, 'modularity/index.html', {'form':form})
