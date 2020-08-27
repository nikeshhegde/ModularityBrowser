import os
with os.add_dll_directory("D:\\UCC Semesters\\Thesis\\Softwares\\SciTools\\bin\\pc-win64"):
    import understand
import logging
import subprocess
import pandas as pd
import numpy as np
import imgkit
"""
Create a understand database from the source code
"""
def create_udb(udb_path, language, project_root):
    try:
        output = subprocess.check_output("und create -db {udb_path} -languages {lang}".format(udb_path=udb_path, lang=language),shell=True)
        #logging.info(output)
        output = subprocess.check_output("und add -db {udb_path} {project}".format(udb_path=udb_path, project=project_root), shell=True)
        #logging.info(output)
        output = subprocess.check_output("und analyze {udb_path}".format(udb_path=udb_path), shell=True)
        #logging.info(output)
    except subprocess.CalledProcessError as e:
        logging.exception(e.output)
        logging.fatal("udb creation failed")
        raise Exception
"""
This function creates dependencies
"""
def execute(name,path,udb_path,type):
    #print('path is '+path)
    #und export -dependencies file csv output.csv myProject.udb


    css = """
    <style type=\"text/css\">
    table {
    color: #333;
    font-family: Helvetica, Arial, sans-serif;
    width: 640px;
    border: 1px solid black;
    }
    td, th {
    border: 1px solid transparent; /* No more visible border */
    height: 30px;
    }
    th {
    background: #DFDFDF; /* Darken header a bit */
    font-weight: bold;
    }
    td {
    background: #FAFAFA;
    text-align: center;
    }
    table tr:nth-child(odd) td{
    background-color: white;
    }
    </style>
    """

    script = """
    <script>
        let table = document.body.firstElementChild;

        for (let i = 0; i < table.rows.length; i++) {
          let row = table.rows[i];
          row.cells[i].style.backgroundColor = 'red';
        }
    </script>
    """

    config = imgkit.config(wkhtmltoimage='D:\\Software\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')

    if type.upper()=='FILE':
        output = subprocess.check_output("und export -dependencies -format short file matrix {path}\\file.csv {udb_path}".format(path=path,udb_path=udb_path),shell=True)
        #logging.info(output)

        df = pd.read_csv(path+'/file.csv')
        #print(list(df.columns))
        #print(list(df.index))
        df.fillna(0, inplace=True)
        df.to_csv(path+'/file.csv',index=False,encoding='utf8')
        # #print(df.head())
        # data = pd.read_csv(open(path+'/file.csv', 'r'),index_col=0)
        #
        # text_file = open(path+'/file.html', "a")
        # # write the CSS
        # text_file.write(css)
        # # write the HTML-ized Pandas DataFrame
        # text_file.write(data.to_html())
        # text_file.write(script)
        # text_file.close()
        #
        # imgkitoptions = {"format": "png"}
        # imgkit.from_file(path+'/file.html', path+'/file.png', options=imgkitoptions,config=config)



    if type.upper()=='CLASS':
        output = subprocess.check_output("und export -dependencies -format short class matrix {path}/class.csv {udb_path}".format(path=path,udb_path=udb_path),shell=True)
        #logging.info(output)

        df1 = pd.read_csv(path+'/class.csv')
        #print(df1.head())
        #print(len(df1))
        #print(len(df1.columns)-1)
        df1.fillna(0, inplace=True)
        df1.to_csv(path+'/class.csv',index=False,encoding='utf8')
        #print(df1.head())
        #data1 = pd.read_csv(open(path+'/class.csv', 'r'),index_col=0)

"""
This function generates reports
"""
def generate_reports(name,path,udb_path):
    file_path = name + '_html/'
    project_metric_file = file_path + 'projmetrics.html'
    #print(project_metric_file)
    output = subprocess.check_output("und report {path}".format(path=udb_path),shell=True)
    #logging.info(output)
    #print("report exported")
