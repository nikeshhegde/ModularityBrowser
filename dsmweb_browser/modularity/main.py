#main file
import sys
import os
with os.add_dll_directory("D:\\UCC Semesters\\Thesis\\Softwares\\SciTools\\bin\\pc-win64"):
    import understand
import requests
import subprocess
import logging
from UnderstandService import create_udb,execute,generate_reports
from ProjectMetrics import generate_metrics
#from .UnderstandService import create_udb,execute
from git import Repo
from github import Github
import configparser
import os
import shutil
import json
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import datetime
import os, shutil
import dateutil.parser as parser

project_path='D:\\code'
dependencies_type = 'FILE'
language='java'
global proj_name
global udb_path
global current_datetime
global since_datetime

#github Authentication using token
headers = {'Authorization':'token b61793fccf8ce2e600a29f5e35c11744255a006c',
        'User-Agent':'https://api.github.com/meta',
        'Content-Type':'application/json'}
#get the fulll project name of the
def get_project_name(search_req):
    pass

def get_repo_url(pull_req): # Get the repo URL to clone the repo
    repo_url=''

    try:
        if pull_req.status_code == 200:
                pull2=pull_req.json()
                repo_url=pull2['items'][0]['html_url']
                #repo_url=pull2[]['html_url']
                #print('Repo_URL:',repo_url)
                #response=requests.get(repo_url,headers=headers)
                #if pull_req.status_code == 200:
                    #repo_url=response.json()['html_url']

    except IndexError as e:
        print('-----------------Exception occured while getting repo url---------------')

    return repo_url

def get_repo_sha(pull_req)    : # Get the repo SHA1 to clone the repo
    sha=''

    try:
        if pull_req.status_code == 200:
                pull_sha=pull_req.json()
                sha=pull_sha[0]['sha']
                #print('SHA1:',sha)
                #response=requests.get(repo_url,headers=headers)
                #if pull_req.status_code == 200:
                    #repo_url=response.json()['html_url']

    except IndexError as e:
        print('-----------------Exception occured while getting repo url---------------')

    return sha

def clone_repo(repo_url,name,num):
    try:
        git_url=repo_url
        #print('git_url is' ,git_url)
        repo_dir=project_path +'\\'+ name+'\\'+str(num)
        if os.path.isdir(repo_dir):
            os.system('rmdir /S /Q "{}"'.format(repo_dir))
        #print('Cloning at:',repo_dir)
        Repo.clone_from(git_url, repo_dir)
        #print('Done cloning')
    except:
        print('Exception occured while cloneing repo', name)

    return repo_dir


#Checkout the version of the project using the SHA for that version
def git_checkout(sha,projectname,num):

        result = []
        flag=True
        path = project_path+'\\'+projectname+'\\'+str(num)+'\\'
        try:
            os.mkdir(path)
        except OSError:
            print ('')
        cmd='git checkout '+ sha
        try:
            process = subprocess.Popen(cmd,cwd=path,shell=TRUE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            #process.stdin.flush()
            result = process.communicate()[1].decode().split(':')[0]
            #stdoutput, stderroutput = process.communicate()
            #print(stderroutput)
            if(result=="FATAL" or result=="fatal"):
                flag=False
            return flag
        except:
            print('')

#def start(req_proj_url,req_language,req_since_date,req_until_date):
def start():
    try:
        #print("code has reached here")
        #proj_name = req_proj_url

        #since_datetime = '2019-08-16T22:16:53Z'
        #until_datetime = '2020-04-20T22:16:53Z'
        #request = 'https://api.github.com/repos/'+repo_name+'/commits?since='+since_datetime+'&until='+until_datetime
        #print('proj_name is '+proj_name)
        #proj_name = 'frandorado/spring-projects'
        #search = 'https://api.github.com/search/repositories?q=repo:yankils/Simple-DevOps-Project'
        search_req = requests.get('https://api.github.com/search/repositories?q=repo:'+proj_name,headers=headers)
        if not search_req.status_code == 200:
            print('Project name:'+proj_name + 'does not exist in GitHub repositories' )
        else:
            projectname=proj_name.split("/")[1]
            print('Project name:'+projectname + ' has been founded in GitHub repositories' )

            # get the repository URL
            repo_url=get_repo_url(search_req)

            #call github service
            github_service(repo_url,proj_name)

    except understand.UnderstandError as e:
        print('Exception occured during processing' + e)
        return 0
        return np

commit_date = []
git_URL = []
sha = []
def github_service(repo_url,proj_name):
    #print("inside github_service")
    #proj_name='nikeshhegde/RoundRobinDataCentre'
    #no_years = 10
    #current_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    #date_no_years_ago = current_datetime - timedelta(years=no_years)
    #print(date_no_years_ago)
    #since_datetime = '2019-11-29T22:16:53Z'
    #current_datetime = '2020-11-31T22:16:53Z'
    request = 'https://api.github.com/repos/'+proj_name+'/commits?since='+since_datetime+'&until='+current_datetime
    #print(request)

    search_req = requests.get(request,headers=headers)
    if search_req.status_code == 200:
        #print("inside 200")
        json_data = search_req.json()
        for data in json_data:
            commit_date.append(data['commit']['author']['date'])
            git_URL.append(data['html_url'])
            sha.append(data['sha'])
    print('Total no of commits in the given date range : '+str(len(sha)))
    if len(sha) == 0:
        print("Try to input some other date range")
    #print(commit_date)
    #print(git_URL[0].rpartition('/commits'))
    if len(sha) > 0:
        projectname=proj_name.split("/")[1]
        print('\nNow checking out the commit version for the project '+projectname +' from the GitHub repository')
        code_checkout(repo_url,sha,projectname)
        print('\nNow generating coupling and cohesion metrics for each commit version')
        generate_metrics(project_path,projectname,len(sha))
        print('\nNow generating matrix for each commit version')
        #call generate matrix function after checking out the versions
        generate_matrix(len(sha),dependencies_type,projectname,commit_date)
        print('\nAll the DSM has been successfully generated.\nPlease start the Django server and visit http://localhost:8000/ and enter project name as ' + projectname + ' and dependency type as ' + dependencies_type )

# function to checkout versions of the code by particular sha
def code_checkout(repo_url,sha,projectname):
    for i in range(len(sha)):
        #Clone the repository
        repo_dir=clone_repo(repo_url,projectname,i)
        print('\nCode checkedout at path: ' +repo_dir)

        #Clone the repository
        flag = git_checkout(sha[i],projectname,i)
        #print(flag)

        udb_path= repo_dir+'\\'+projectname
        file_path = project_path+projectname+'\\'+str(i)
        create_udb(r''+udb_path, language, repo_dir)
        udb_path=r''+udb_path+'.udb'
        #print('udb path is ' + path)

        try:
            db = understand.open(udb_path)
        except understand.UnderstandError as e:
            logging.fatal('udb open failed')
            raise Exception
        #Executing Understand analysis
        execute(projectname,repo_dir,udb_path,dependencies_type)
        generate_reports(projectname,repo_dir,udb_path)
        db.close()


# stores the vertices in the graph
vertices = []
graph = []
vertices_no = 0
y_axis_vertices = []
# Add a vertex to the set of vertices and the graph
def add_vertex(v):
  global graph
  global vertices_no
  global vertices
  if v in vertices:
      print("Vertex ", v, " already exists")
  else:
    vertices_no = vertices_no + 1
    #print("vertices_no == "+str(vertices_no))
    vertices.append(v)
    #graph.clear()
    if vertices_no > 1:
        for vertex in graph:
            vertex.append(0.0)
    #print(graph)
    temp = []
    for i in range(len(vertices)):
        temp.append(0.0)
    graph.append(temp)
    #print(graph)

# Add an edge between vertex v1 and v2 with edge weight e
def add_edge(v1, v2, e):
    global graph
    global vertices_no
    global vertices
    # print("---v1---"+v1)
    # print("---v2--"+v2)
    # print("---===========--")
    # Check if vertex v1 is a valid vertex
    if v1 not in vertices:
        print("Vertex ", v1, " does not exist.")
    # Check if vertex v1 is a valid vertex
    elif v2 not in vertices:
        print("Vertex ", v2, " does not exist.")
    # Since this code is not restricted to a directed or
    # an undirected graph, an edge between v1 v2 does not
    # imply that an edge exists between v2 and v1
    else:
        #print("called here -----------")
        index1 = vertices.index(v1)
        index2 = vertices.index(v2)
        graph[index1][index2] = e


def generate_matrix(sha,dependencies_type,projectname,commit_date):
    if dependencies_type.upper()=='FILE':
        filetype='file'
    elif dependencies_type.upper()=='CLASS':
        filetype='class'
    #total_dir = len(sha)
    img_file_path = 'D://Pyhton/ModularityBrowser/dsmweb_browser/modularity/static/modularity/images/'
    #img_file_path = 'D:\\code\\'+projectname+'\\images\\'
    for filename in os.listdir(img_file_path):
        file_path = os.path.join(img_file_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    for i in range(sha):
        #print(i)
        if i < sha:
            #file_path = 'D:\\code\\'+projectname+'\\'
            #try:
            #    os.mkdir(img_file_path)
            #except OSError:
            #    print ("Creation of the directory %s failed" % img_file_path)
            #else:
            #    print ("Successfully created the directory %s " % img_file_path)
            file_path = 'D:\\code\\'+projectname+'\\'+str(i)
            #print(file_path)
            #file_path2 = file_path+str(i+1)
            file1 = file_path+'\\'+filetype+'.csv'
            #file2 = file_path2+'\\class.csv'
            #print(file1)
            #print(file2)
            #print('----------')
            #f1 = pd.read_csv(file1)
            #f2 = pd.read_csv(file2)
            #file_path = 'D:\\code\\RoundRobinDataCentre\\0\\class.csv'
            #file_path1 = 'D:\\code\\RoundRobinDataCentre\\1\\class.csv'
            with open(file1,'rt') as f:
                vertices.clear()
                graph.clear()
                y_axis_vertices.clear()
                vertices_no = 0
                #print("initial")
                #print(vertices)
                #print(graph)
                #data = ''
                #fileObject = csv.reader(f)
                #row_count = sum(1 for row in fileObject)
                #print(row_count)
                data = csv.reader(f)
                headers = list(next(data))  # gets the first line
                #print(headers)
                for j in range(len(headers)):
                    if j > 0:
                        #vertices.append(headers[i])
                        #vertices_no = 0
                        add_vertex(headers[j])

                #print(vertices_no)
                # sort the graph
                #vertices.sort()
                #print("here ")
                #print("after adding vertex")
                #print(vertices)
                #print(graph)

                #print("after adding edge")
                for row in data:
                    values = list(row)
                    #print("-------------values-----------")
                    #print(values)
                    for k in range(len(values)):
                        if k == 0:
                            vertex_name = values[0]
                        else:
                            #print(i)
                            add_edge(vertex_name,vertices[k-1],float(values[k]))
                            #print(vertices)
                            #print(graph)
                            # print("----------------")

                len_vertices = len(vertices)
                for l in range(len(vertices)):
                    vertices[l] = vertices[l]+'_'+str(l)
                    #print(vertices[i])
                    y_axis_vertices.append(l)
                #print(y_axis_vertices)
                # Display matrix
                fig, ax = plt.subplots(figsize=(20.48,10.80))
                im = ax.imshow(graph,cmap=plt.get_cmap('binary'),aspect='auto')
                #im = ax.imshow(graph,aspect='auto')
                ax.set_xticks(np.arange(len(y_axis_vertices)))
                ax.set_yticks(np.arange(len(y_axis_vertices)))
                ax.set_xticklabels(y_axis_vertices)
                ax.set_yticklabels(vertices)
                ax.xaxis.tick_top()


                ##
                N = 150
                plt.gca().margins(x=0)
                plt.gcf().canvas.draw()
                tl = plt.gca().get_xticklabels()
                maxsize = max([t.get_window_extent().width for t in tl])
                m = 0.2 # inch margin
                s = maxsize/plt.gcf().dpi*N+2*m
                margin = m/plt.gcf().get_size_inches()[0]

                plt.gcf().subplots_adjust(left=margin, right=1.-margin)
                plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

                ###
                # Loop over data dimensions and create text annotations.
                for m in range(len_vertices):
                    for n in range(len_vertices):
                        text = ax.text(n, m, graph[m][n],
                                       ha="center", va="center",color="w",fontsize=10)
                fig.tight_layout()
                #plt.axline(0,0, linewidth=4, color='r')
                #plt.title(commit_date[i])
                plt.savefig(img_file_path +'/'+filetype+'_'+str(i)+'.png')
                print('Displaying Dependency Structure Matrix(DSM) for commit version: ' + commit_date[i])
                plt.show()
                print('Dependency Structure Matrix(DSM) for commit version at file path: ' + file_path +' has been generated')
                #plt.matshow(graph,0)
                #plt.show()
if __name__ == '__main__':
    proj_name = str(sys.argv[1])
    dependencies_type = str(sys.argv[2]).upper()
    since_datetime = str(sys.argv[3])
    if len(since_datetime) < 20:
        since_datetime = parser.parse(since_datetime).strftime("%Y-%m-%dT%H:%M:%SZ")
    current_datetime = str(sys.argv[4])
    if len(current_datetime) < 20:
        current_datetime = parser.parse(current_datetime).strftime("%Y-%m-%dT%H:%M:%SZ")

    #print(since_datetime)
    #print(current_datetime)
    #datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    #proj_name = 'nikeshhegde/RoundRobinDataCentre'
    start()
    #get_differences(8)
