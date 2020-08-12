import requests
import pandas as pd
import os
import time

path = os.getcwd()

##TODO: Replace filename with current input (must have dea_num column but okay to leave rows blank)
df = pd.read_csv(os.path.join(path, 'data', 'CURRENT_INPUT.csv'), index_col=False)
npi_data = df['dea_num'].values.tolist()
npi_data = ["None" if type(x) == float else str(x) for x in npi_data]
url = 'https://www.samhsa.gov/bupe/lookup-form'
samhsa_data_list = []
counter = 1
for index, row in df.iterrows():
        if counter % 100 == 0:
            time.sleep(300)
        counter +=1
        print(str(int(index)+1), row['npi'])
        dea_number = 'A*' if type(row['dea_num']) == float else str(row['dea_num'])
        data = {'practitioner': row['lastname'],
            'dea_number': dea_number,
            'form_build_id': 'form-MLgZu20sRJX2-p5eYVmVnVpZfuTyu5DgBYQJEVHe1I8',
            'form_id': 'bupe_pharm_lookup',
            'op': 'Submit'}
        page = requests.post(url,data).text
        data_list = []
        data_string = page.split('\\u003Cli class=\\u0022messages__item\\u0022\\u003E')[1:]
        for data in data_string:
            data_list.append(data.split('\\u003C\\/li\\u003E\\n ')[0])
        samsha_data = {}
        if "is not a Buprenorphine Certified Physician" in page:
            samsha_data['Full Name'] = "Name not found at all"
            samsha_data['Job'] = "NYI"
            samsha_data['DEA Registration Number'] = "maybe expired"
            samsha_data['Licensed State'] = "NYI"
            samsha_data['Date Certified'] = "NYI"
            samsha_data['Waiver Count'] = "NYI"
        else:
            if data_list[0].split(' is a')[0] == (row['firstname'] + ' ' + row['lastname']):
                samsha_data['Full Name'] = data_list[0].split(' is a')[0]
                samsha_data['Job'] = data_list[0].split(' is a ')[1][:-2]
                samsha_data['DEA Registration Number'] = data_list[1].split(': ')[1]
                samsha_data['Licensed State'] = data_list[2].split(': ')[1]
                samsha_data['Date Certified'] = data_list[3].split(': ')[1]
                samsha_data['Waiver Count'] = data_list[4].split('for ')[1].split(' patients')[0]
            else:
                samsha_data['Full Name'] = "Found different name"
                samsha_data['Job'] = "NYI"
                samsha_data['DEA Registration Number'] = "NYI"
                samsha_data['Licensed State'] = "NYI"
                samsha_data['Date Certified'] = "NYI"
                samsha_data['Waiver Count'] = "NYI"
        # print(samsha_data)
        samhsa_data_list.append(samsha_data)
final_df = pd.DataFrame(samhsa_data_list)
df = df.reset_index(drop=True)
final_df = pd.concat([df, final_df], axis=1)
final_df.to_csv(os.path.join(path, 'data', 'xwaivers_yyyy-mm-dd_numnames_.csv'), index=False)
