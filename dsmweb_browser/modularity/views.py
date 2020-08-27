import os
with os.add_dll_directory("D:\\UCC Semesters\\Thesis\\Softwares\\SciTools\\bin\\pc-win64"):
    import understand
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import GitHubForm
from PIL import Image
import glob
import fnmatch

project_path='D://code'
# Create your views here.
def index(request):

    if request.method=='POST':
        form = GitHubForm(request.POST)
        if form.is_valid():
            project_url = form.cleaned_data['project_url']
            dependencies_type = form.cleaned_data['dependencies_type']



            img_path = project_path + '/' + project_url + '/' + 'images'
            print(img_path)
            if dependencies_type.upper() == 'FILE':
                img_pre = 'file_'
            else:
                img_pre = 'class_'
            image_list = []

            #path = 'modularity/static/modularity/images'+project_url
            pattern = img_pre+'*.png'
            for root, dirs, files in os.walk('modularity/static/modularity/images'):
                #print ("Current directory", root)
                #print ("Sub directories", dirs)
                #print ("Files", files)
                for file in files:
                    if fnmatch.fnmatch(file, pattern):
                        image_list.append(file)
            #print(image_list)
            #for filename in glob.glob(os.path.join(img_path,img_pre+'*.png')): #assuming gif
            #    print(filename)
                #im=Image.open(filename)
                #image_list.append(filename)

            #start(project_url,language_type,since_datetime,until_datetime)
            context = {
            'project_url': project_url,
            'dependencies_type': dependencies_type,
            'image_list': image_list
            }
            template = loader.get_template('modularity/github_data.html')

            return HttpResponse(template.render(context, request))

    else:
        form = GitHubForm()
    return render(request, 'modularity/index.html', {'form':form})
