#main file

import os
with os.add_dll_directory("D:\\UCC Semesters\\Thesis\\Softwares\\SciTools\\bin\\pc-win64"):
    import understand
import requests
import subprocess
import logging
from UnderstandService import create_udb,execute
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

#repo_name='nikeshhegde/RoundRobinDataCentre'
#proj_name = 'nikeshhegde/RoundRobinDataCentre'
project_path='D:\\code'


#github Authentication using token
headers = {'Authorization':'token 6c03934cde39dde8d6050584ca9e9011d8b42c85',
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
        print('git_url is' ,git_url)
        repo_dir=project_path +'\\'+ name+'\\'+str(num)
        if os.path.isdir(repo_dir):
            os.system('rmdir /S /Q "{}"'.format(repo_dir))

        print('Cloning at:',repo_dir)
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
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

        cmd='git checkout '+ sha
        try:
            process = subprocess.Popen(cmd,cwd=path,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            result = process.communicate()[1].decode().split(':')[0]
            print(result)
            if(result=="FATAL" or result=="fatal"):
                flag=False
            return flag
        except:
            print('Exception occured during processing')

def start():
    try:

        since_datetime = '2019-08-16T22:16:53Z'
        until_datetime = '2020-04-20T22:16:53Z'
        #request = 'https://api.github.com/repos/'+repo_name+'/commits?since='+since_datetime+'&until='+until_datetime

        proj_name = 'nikeshhegde/RoundRobinDataCentre'
        #search = 'https://api.github.com/search/repositories?q=repo:yankils/Simple-DevOps-Project'
        search_req = requests.get('https://api.github.com/search/repositories?q=repo:'+proj_name,headers=headers)
        #print(search_req.json())
        projectname=proj_name.split("/")[1]
        print('Project name:',projectname)

        # get the repository URL
        repo_url=get_repo_url(search_req)

        #call github service
        test_github_service(repo_url)


    except understand.UnderstandError as e:
        print('Exception occured during processing' + e)
        return 0
        return np

def test_github_service(repo_url):
    print("inside test_github_service")
    repo_name='nikeshhegde/RoundRobinDataCentre'
    since_datetime = '2019-11-29T22:16:53Z'
    until_datetime = '2020-04-20T22:16:53Z'
    request = 'https://api.github.com/repos/'+repo_name+'/commits?since='+since_datetime+'&until='+until_datetime
    print(request)
    commit_date = []
    git_URL = []
    sha = []
    search_req = requests.get(request,headers=headers)
    if search_req.status_code == 200:
        print("inside 200")
        json_data = search_req.json()
        for data in json_data:
            commit_date.append(data['commit']['author']['date'])
            git_URL.append(data['html_url'])
            sha.append(data['sha'])
    print(len(sha))
    #print(git_URL[0].rpartition('/commits'))
    projectname=repo_name.split("/")[1]
    print('Project name:',projectname)
    code_versions(repo_url,sha,projectname)

# function to checkout versions of the code by particular sha
def code_versions(repo_url,sha,projectname):
    for i in range(len(sha)):
        #Clone the repository
        repo_dir=clone_repo(repo_url,projectname,i)
        print("repo_dir " +repo_dir)

        #Clone the repository
        flag = git_checkout(sha[i],projectname,i)
        print(flag)

        udb_path=repo_dir
        project_root=repo_dir
        language='java'
        udb_path= udb_path+'\\'+projectname
        print('path is ' + r''+udb_path)

        create_udb(r''+udb_path, language, project_root)
        path=r''+udb_path+'.udb'
        print('udb path is' + path)


        try:
            db = understand.open(path)

        except understand.UnderstandError as e:
            logging.fatal('udb open failed')
            raise Exception

        print('before executing.....')
        # get the type of dependencies required
        type = 'CLASS'
        #Executing Understand analysis
        execute(db,projectname,repo_dir,path,type)

        db.close()

# stores the vertices in the graph
vertices = []
graph = []
vertices_no = 0
# Add a vertex to the set of vertices and the graph
def add_vertex(v):
  global graph
  global vertices_no
  global vertices
  if v in vertices:
    print("Vertex ", v, " already exists")
  else:
    vertices_no = vertices_no + 1
    vertices.append(v)
    if vertices_no > 1:
        for vertex in graph:
            vertex.append(0)
    temp = []
    for i in range(vertices_no):
        temp.append(0.0)
    graph.append(temp)

# Add an edge between vertex v1 and v2 with edge weight e
def add_edge(v1, v2, e):
    global graph
    global vertices_no
    global vertices
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
        index1 = vertices.index(v1)
        index2 = vertices.index(v2)
        graph[index1][index2] = e


def get_differences(sha):

    #total_dir = len(sha)
    for i in range(sha):
        #print(i)
        if i < sha:
            file_path = 'D:\\code\\RoundRobinDataCentre\\'
            file_path = file_path+str(i)
            #print(file_path)
            #file_path2 = file_path+str(i+1)
            file1 = file_path+'\\class.csv'
            #file2 = file_path2+'\\class.csv'
            #print(file1)
            #print(file2)
            #print('----------')
            #f1 = pd.read_csv(file1)
            #f2 = pd.read_csv(file2)
            #file_path = 'D:\\code\\RoundRobinDataCentre\\0\\class.csv'
            #file_path1 = 'D:\\code\\RoundRobinDataCentre\\1\\class.csv'
            with open(file1,'rt') as f:
                #fileObject = csv.reader(f)
                #row_count = sum(1 for row in fileObject)
                #print(row_count)
                data = csv.reader(f)
                headers = list(next(data))  # gets the first line
                for i in range(len(headers)):
                    if i > 0:
                        #vertices.append(headers[i])
                        add_vertex(headers[i])
                        #print(vertices)
                #print(vertices_no)
                # sort the graph
                #vertices.sort()
                #print(vertices)
                #print(graph)
                for row in data:
                    values = list(row)
                    #print(values)
                    for i in range(len(values)):
                        if i == 0:
                            vertex_name = values[0]
                        else:
                            #print(i)
                            add_edge(vertex_name,vertices[i-1],float(values[i]))
                #print(graph)
                # Display matrix
                fig, ax = plt.subplots()
                im = ax.imshow(graph)
                ax.set_xticks(np.arange(len(vertices)))
                ax.set_yticks(np.arange(len(vertices)))
                ax.set_xticklabels(vertices)
                ax.set_yticklabels(vertices)
                ax.xaxis.tick_top()
                # Loop over data dimensions and create text annotations.
                for i in range(len(vertices)):
                    for j in range(len(vertices)):
                        text = ax.text(j, i, graph[i][j],
                                       ha="center", va="center", color="w")
                # Rotate the tick labels and set their alignment.
                plt.setp(ax.get_xticklabels(), rotation=45, ha="left",
                         rotation_mode="anchor")
                fig.tight_layout()
                #file_path = 'D:\\code\\RoundRobinDataCentre\\0\\'
                #if not os.path.isdir(results_dir):
                    #os.makedirs(results_dir)
                #pdf.savefig(fig)
                #print(file_path)
                plt.savefig(file_path +'/imageclass.png')
                #plt.show()
                #plt.matshow(graph,0)
                #plt.show()
if __name__ == '__main__':
    #start()
    get_differences(8)
