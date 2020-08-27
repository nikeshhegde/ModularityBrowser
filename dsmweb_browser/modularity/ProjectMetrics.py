from bs4 import BeautifulSoup

def generate_metrics(project_path,projectname,sha):
    name = []
    values = []
    headers = []
    lcom_values = []
    cbo_values = []
    lcom_values_list = []
    cbo_values_list = []
    for i in range(sha):
        file_path = project_path+'\\'+projectname+'\\'+str(i)+'\\'+projectname+'_html\\classoom_C.html'
        soup = BeautifulSoup(open(file_path),features="html.parser")
        html_metrics_table = soup.find("table", {'id':'metrics-table'})
        #ths = html_metrics_table.find_all('th')
        #print(ths)
        #for th in ths:
        #    headers.append(th.get_text())
        #print(headers)
        trs = html_metrics_table.find_all('tr')
        for tr in trs:
            #ths = tr.find_all('th')
            #print(ths[0].get_text())
            tds = tr.find_all('td')
            #headers.append(ths.get_text())
            #name.append(tds[0].get_text())
            for td in tds:
                values.append(td.get_text())
            #print(values)
            if not len(values)==0:
                if not int(values[1])==0:
                    lcom_values.append(int(values[1]))
                if not int(values[4])==0:
                    cbo_values.append(int(values[4]))
            values.clear()
        lcom_sum = sum(lcom_values)
        cbo_sum = sum(cbo_values)
        final_lcom = 1 - (lcom_sum / len(lcom_values) * 0.01)
        final_cbo = cbo_sum / len(cbo_values)
        final_lcom = round(final_lcom, 2)
        final_cbo = round(final_cbo, 2)
        #print(final_lcom)
        #print(final_cbo)
        lcom_values_list.append(final_lcom)
        cbo_values_list.append(final_cbo)
        lcom_values.clear()
        cbo_values.clear()
    average_lcom = round(Average(lcom_values_list),2)
    average_cbo = round(Average(cbo_values_list),2)
    print('Average LCOM values for the period ')
    print(average_lcom)
    print('Average CBO values for the period ')
    print(average_cbo)
    if average_cbo >=1 and average_cbo <=4:
        print('\n\nAn average value of Count of Coupled class (CBO) between 1 and 4 is good, \nsince it indicates that the classes are loosely coupled')
        print('\n\nIn the duration of time chosen, the project has overall Low Coupling for the duration of time for value : '+str(average_cbo))
    else:
        print('\n\nIn the duration of time chosen, the project has overall High Coupling for the duration of time for value : '+str(average_cbo))

    print('\n\nA value of Percent Lack of Cohesion(LCOM) ranges from 0 and 1, and closest to 0 indicates High Cohesion between the classes')
    print('\nIn the duration of time chosen, the project has LCOM value : '+str(average_lcom))

# Python program to get average of a list
def Average(lst):
    return sum(lst) / len(lst)
