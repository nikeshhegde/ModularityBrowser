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

repo_name='nikeshhegde/RoundRobinDataCentre'
proj_name = 'nikeshhegde/RoundRobinDataCentre'
project_path='D:\\code'


#github Authentication using token
headers={'Authorization':'token fae07fdf65253e14cb1f2f80235fd11ebb599e4c',
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
                print('Repo_URL:',repo_url)
                #response=requests.get(repo_url,headers=headers)
                #if pull_req.status_code == 200:
                    #repo_url=response.json()['html_url']

    except IndexError as e:
        print('-----------------Exception occured while getting repo url---------------')

    return repo_url

def get_repo_sha(pull_req)    : # Get the repo URL to clone the repo
    sha=''

    try:
        if pull_req.status_code == 200:
                pull_sha=pull_req.json()
                sha=pull_sha[0]['sha']
                print('SHA1:',sha)
                #response=requests.get(repo_url,headers=headers)
                #if pull_req.status_code == 200:
                    #repo_url=response.json()['html_url']

    except IndexError as e:
        print('-----------------Exception occured while getting repo url---------------')

    return sha

def clone_repo(repo_url,name):
    try:
        git_url=repo_url
        print('git_url is' ,git_url)
        repo_dir=project_path +'\\'+ name
        if os.path.isdir(repo_dir):
            os.system('rmdir /S /Q "{}"'.format(repo_dir))

        print('Cloning at:',repo_dir)
        Repo.clone_from(git_url, repo_dir)
        #print('Done cloning')
    except:
        print('Exception occured while cloneing repo', name)

    return repo_dir


#Checkout the version of the project using the SHA for that version
def git_checkout(sha,projectname):

        result = []
        flag=True
        path = project_path+'\\'+projectname
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
        #search_req = requests.get('https://api.github.com/search/repositories?q=repo:'+proj_name,headers=headers)

        projectname=proj_name.split("/")[1]
        print('Project name:',projectname)

        # get the repository URL
        #repo_url=get_repo_url(search_req)

        #Clone the repository
        #repo_dir1=clone_repo(repo_url,projectname)

        #pull_req = requests.get('https://api.github.com/repos/'+proj_name+'/commits?since='+since_datetime+'&until='+until_datetime,headers=headers)

        # get the repository URL
        #repo_sha=get_repo_sha(search_req)
        #print(repo_url)

        #Clone the repository
        #flag = git_checkout(repo_sha,projectname)
        #print(flag)
        repo_dir1='D:\\code\\RoundRobinDataCentre'

        udb_path=repo_dir1
        project_root=repo_dir1
        language='java'

        print('path is' + r''+udb_path)

        #create_udb(r''+udb_path+'\\'+projectname, language, project_root)
        path1=r''+udb_path+'\\'+projectname+'.udb'
        print('udb path is' + path1)

        try:
            db1 = understand.open(path1)

        except understand.UnderstandError as e:
            logging.fatal('udb open failed')
            raise Exception

        print('before executing.....')
        #Executing Understand analysis
        execute(db1,projectname,repo_dir1,path1)

        db1.close()




    except understand.UnderstandError as e:
        print('Exception occured during processing' + e)
        return 0
        return np

if __name__ == '__main__':
    start()
