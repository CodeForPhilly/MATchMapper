import requests
import lxml.html as lh
import pandas as pd
import os

def adjust_phone_format(phone_number):
    if len(phone_number) > 0 and phone_number[0] == "#":
        phone_number = phone_number[2:]
        phone_number = phone_number.replace(")","-")
    return phone_number

path = os.getcwd()

df = pd.read_csv(path + '\\hfp.csv', index_col=False)
df.columns = df.iloc[0]
df = df[1:]
npi_data = df['npi'].values.tolist()
df = df[['who_id']]
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
                    npi_dict['Full Name'] = substring.split(' Other Name: ')[0]
                    print(npi_dict['Full Name'])
                    npi_dict['Other Name'] = substring.split('Other Name: ')[1].split(' Gender')[0]
                else:
                    substring = " ".join(t.text_content().split())
                    npi_dict['Full Name'] = substring.split(' Gender: ')[0]
                    print(npi_dict['Full Name'])
                    npi_dict['Other Name'] = ""  
        npi_dict['Gender'] = gender_info.split(' ')[1]
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
            if temp_list[0] == "Mailing Address":
                mailing_address = temp_list[1].split(" Phone")[0]
                mailing_address_phone = temp_list[1].split(" Phone:")[1].split("|")[0].replace(" ","")
                mailing_address_fax = temp_list[1].split("Fax:")[1].split("View Map")[0].replace(" ","")
                npi_dict['Mailing Address'] = mailing_address
                npi_dict['Mailing Address Phone'] = adjust_phone_format(mailing_address_phone)
                npi_dict['Mailing Address Fax'] = mailing_address_fax
            elif temp_list[0] == "Primary Practice Address":
                primary_practice_address = temp_list[1].split(" Phone")[0]
                primary_practice_address_phone = temp_list[1].split(" Phone:")[1].split("|")[0].replace(" ","")
                primary_practice_address_fax = temp_list[1].split("Fax:")[1].split("View Map")[0].replace(" ","")
                npi_dict['Primary Practice Address'] = primary_practice_address
                npi_dict['Primary Practice Address Phone'] = adjust_phone_format(primary_practice_address_phone)
                npi_dict['Primary Practice Address Fax'] = primary_practice_address_fax 
            elif temp_list[0] == "Other Identifiers":
                if temp_list[1] == "Issuer State Number":
                    npi_dict['Issuer Info'] = ""
                else:
                    medicaid_list = temp_list[1].split("MEDICAID ")[1:]
                    if len(medicaid_list) > 1:
                        npi_dict['Issuer Info'] = "| ".join(medicaid_list)
                    elif len(medicaid_list) == 1:
                        npi_dict['Issuer Info'] = medicaid_list[0]
                    else:
                        raise ValueError("something unexpected with Medicaid input")
            elif temp_list[0] == "Taxonomy":
                if temp_list[1].split(" ")[-1] == "Number":
                    npi_dict['Primary Taxonomy'] = ""
                    npi_dict['Primary Taxonomy Code'] = ""
                    npi_dict['Primary Taxonomy State'] = ""
                    npi_dict['Primary Taxonomy License'] = ""   
                # assuming that there will always be at least one primary taxonomy (as the first taxonomy data) if there is any taxonomy data
                else:
                    data_without_header = temp_list[1].split("Yes ")[1]
                    if "No" in data_without_header:
                        data = data_without_header.split(" No")[0]
                    else:
                        data = data_without_header
                    primary_taxon_code = data.split(" - ")[0]
                    remaining_data = data.split(" - ")[1].split(" ")
                    primary_taxon_license = remaining_data[-1] if len(remaining_data[-2]) == 2 else ""
                    primary_taxon_state = remaining_data[-2] if len(remaining_data[-2]) == 2 else ""
                    primary_taxon = " ".join(remaining_data[:-2]) if len(remaining_data[-2]) == 2 else " ".join(remaining_data)  
                    npi_dict['Primary Taxonomy'] = primary_taxon
                    npi_dict['Primary Taxonomy Code'] = primary_taxon_code
                    npi_dict['Primary Taxonomy State'] = primary_taxon_state
                    npi_dict['Primary Taxonomy License'] = primary_taxon_license                    
            elif temp_list[0] in ['NPI', 'Enumeration Date', 'NPI Type', 'Sole Proprietor', 'Status', 'Secondary Practice Address']:    
                if temp_list[0] == 'Secondary Practice Address':
                    npi_dict[temp_list[0]] =temp_list[1].split(" Phone")[0]
                else:
                    npi_dict[temp_list[0]] = temp_list[1]   
                         
        npi_final_data.append(npi_dict)
final_df = pd.DataFrame(npi_final_data)
# final_df = final_df.drop(['Name'], axis=1)
# final_df.columns = ['Last Updated','Certification Date','NPI','Enumeration Date','NPI Type','Sole Proprietor','Status','Mailing Address','Primary Practice Address','Health Information Exchange','Other Identifiers','Taxonomy','Yes','','No','MEDICAID','Secondary Practice Address']
df.columns = ['who_id']
df = df.reset_index(drop=True)
final_df = pd.concat([df, final_df], axis=1)
final_df.to_csv(path + "\\final_hfp.csv", index=False)

