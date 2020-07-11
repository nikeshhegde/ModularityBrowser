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
		logging.info(output)
		output = subprocess.check_output("und add -db {udb_path} {project}".format(udb_path=udb_path, project=project_root), shell=True)
		logging.info(output)
		output = subprocess.check_output("und analyze {udb_path}".format(udb_path=udb_path), shell=True)
		logging.info(output)
	except subprocess.CalledProcessError as e:
		logging.exception(e.output)
		logging.fatal("udb creation failed")
		raise exception
"""
This function creates dependencies
"""
def execute(db,name,path,udb_path,type):
    language='java'
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
        output = subprocess.check_output("und export -dependencies -format short file matrix {path}/file.csv {udb_path}".format(path=path,udb_path=udb_path),shell=True)
        logging.info(output)

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
        logging.info(output)

        df1 = pd.read_csv(path+'/class.csv')
        #print(df1.head())
        #print(len(df1))
        #print(len(df1.columns)-1)
        df1.fillna(0, inplace=True)
        df1.to_csv(path+'/class.csv',index=False,encoding='utf8')
        #print(df1.head())
        #data1 = pd.read_csv(open(path+'/class.csv', 'r'),index_col=0)



        # text_file1 = open(path+'/class.html', "a")
        # # write the CSS
        # text_file1.write(css)
        # # write the HTML-ized Pandas DataFrame
        # text_file1.write(data1.to_html())
        # text_file1.write(script)
        # text_file1.close()
        #
        # imgkitoptions = {"format": "png"}
        # imgkit.from_file(path+'/class.html',path+'/class.png', options=imgkitoptions,config=config)



    # type='.java'
    # size = len(type)
    # #print('here')
    # #fileset = get_filenames(db,type)
    # #print(fileset)
    # relationship = dict()
    # longnames = []
    # try:
    #     for entity in db.ents():
    #         if entity.longname()[(-1*size):]==type:
    #             relationship[entity.name()] = entity.depends()
    #             #longnames.append(entity.longname())
    #             #print(entity.filerefs())
    #     #print(relationship)
    #     #print(len(relationship))
    #     headers = list(relationship.keys())
    #     #values = list(relationship.values())
    #     #print(longnames)
    #     print(headers)
    #     #print(values)
    #     #for d in relationship:
    #         #print(relationship.values())
    #     #print(len(values))
    #
    #     # list[ key : list[] ]
    #
    #     #dsm_matrix = [[0 for i in range(len(values))] for j in range(len(values))]
    #
    #     #for i in range(len(values)):
    #     #    for
    #
    #     y = dict()
    #     for key, v  in relationship.items():
    #         new_list = []
    #         new_list.append(v)
    #         #print(key)
    #         #print(new_list)
    #         #for i in range(len(new_list)):
    #             #for k in new_list[i]:
    #                 #print('key is ' + key)
    #                 #print('relation is ')
    #                 #print(k)
    #                 #print('value is ')
    #                 #print(len(new_list[i][k]))
    #                 #y[k] = len(new_list[i][k])
    #                 #print(y)
    #                 #dsm = dict()
    #                 #dsm[key+k] = len(new_list[i][k])
    #             #y = dict()
    #
    #
    #     #am = pd.DataFrame(np.zeros(shape=(5,5)), columns=list(headers), index=list(headers))
    #     #print(am)
    #     #print(path)
    #     #am.to_csv(path+'\\file.csv')
    #
    #
    #
    #
    # except understand.UnderstandError as e:
    #     print(e)
