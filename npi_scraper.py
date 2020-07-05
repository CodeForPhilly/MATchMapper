import requests
import lxml.html as lh
import pandas as pd
import os

path = os.getcwd()

df = pd.read_csv(path + '\\hfp.csv', index_col=False)
df.columns = df.iloc[0]
df = df[1:]
df = df[['firstname','lastname','who_id','npi']]
npi_data = df['npi'].values.tolist()
# npi_data = ['1205954138']
npi_final_data = []
for npi_id in npi_data:
    if type(npi_id) == str:
        npi_dict = {}
        url = 'https://npiregistry.cms.hhs.gov/registry/provider-view/' + npi_id

        page = requests.get(url)
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//tr')
        el_elements = doc.xpath("//div[@class='row-fluid']")
        gender_elements = doc.xpath("//span[@class='style1']")
        gender_info = " ".join(gender_elements[0].text_content().split())
        npi_dict['Gender'] = gender_info.split(' ')[1]
        # case_num is 0 if the person has no other name. case_num is 1 if the person has other name
        case_num = 1
        i=0
        for t in tr_elements[0]:
            i+=1
            name = t.text_content()
            if i == 3:
                case_num = 0 if name == "Last Updated:" else 1
        i = 0
        for t in el_elements[0]:
            i+=1
            if i==2:
                if case_num == 1:
                    substring = " ".join(t.text_content().split())
                    npi_dict['Name'] = substring.split('Other Name: ')[0]
                    npi_dict['Other Name'] = substring.split('Other Name: ')[1].split(' Gender')[0]
                else:
                    substring = " ".join(t.text_content().split())
                    npi_dict['Name'] = substring.split('Gender: ')[0]
                    npi_dict['Other Name'] = ""           
       
        i=0
        for t in tr_elements[case_num]:
            i+=1
            name=t.text_content()
            if i == 5:
                npi_dict['Last Updated'] = name
        i=0
        for t in tr_elements[case_num+1]:
            i+=1
            name=t.text_content()
            name = " ".join(name.split())
            if i == 3:
                npi_dict['Certification Date'] = name
        for row in tr_elements[case_num+2:]:
            temp_list = []
            for t in row:
                name = t.text_content()
                name = " ".join(name.split())
                temp_list.append(name)
            npi_dict[temp_list[0]] = temp_list[1]        
        npi_final_data.append(npi_dict)
final_df = pd.DataFrame(npi_final_data)
final_df = final_df.drop(['Name'], axis=1)
# final_df.columns = ['Last Updated','Certification Date','NPI','Enumeration Date','NPI Type','Sole Proprietor','Status','Mailing Address','Primary Practice Address','Health Information Exchange','Other Identifiers','Taxonomy','Yes','','No','MEDICAID','Secondary Practice Address']
df.columns = ['firstname','lastname','who_id','npi']
df = df.reset_index(drop=True)
final_df = pd.concat([df, final_df], axis=1)
final_df.to_csv(path + "\\final_hfp.csv", index=False)

