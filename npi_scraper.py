import requests
import lxml.html as lh
import pandas as pd
import os

path = os.getcwd()

df = pd.read_csv(path + '\\hfp.csv', index_col=False)
df.columns = df.iloc[0]
df = df[1:]
npi_data = df['npi'].values.tolist()
npi_final_data = []
for npi_id in npi_data:
    print(npi_id)
    if type(npi_id) == str:
        url = 'https://npiregistry.cms.hhs.gov/registry/provider-view/' + npi_id

        page = requests.get(url)
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//tr')
        npi_dict = {}
        i=0
        for t in tr_elements[0]:
            i+=1
            name=t.text_content()
            if i == 5:
                npi_dict['Last Updated'] = name
        i=0
        for t in tr_elements[1]:
            i+=1
            name=t.text_content()
            name = " ".join(name.split())
            if i == 3:
                npi_dict['Certification Date'] = name
        for row in tr_elements[2:]:
            temp_list = []
            for t in row:
                name = t.text_content()
                name = " ".join(name.split())
                temp_list.append(name)
            npi_dict[temp_list[0]] = temp_list[1]        
        npi_final_data.append(npi_dict)
print(npi_final_data)

