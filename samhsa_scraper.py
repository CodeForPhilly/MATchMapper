import requests

url = 'https://www.samhsa.gov/bupe/lookup-form'
data = {'practitioner': 'Kravinsky',
    'dea_number': 'A*',
    'form_build_id': 'form-MLgZu20sRJX2-p5eYVmVnVpZfuTyu5DgBYQJEVHe1I8',
    'form_id': 'bupe_pharm_lookup',
    'op': 'Submit'}
page = requests.post(url,data).text
data_list = []
data_string = page.split('\\u003Cli class=\\u0022messages__item\\u0022\\u003E')[1:]
for data in data_string:
    data_list.append(data.split('\\u003C\\/li\\u003E\\n ')[0])
samsha_data = {}
samsha_data['Full Name'] = data_list[0].split(' is a')[0]
samsha_data['Job'] = data_list[0].split(' is a ')[1][:-2]
samsha_data['DEA Registration Number'] = data_list[1].split(': ')[1]
samsha_data['Licensed State'] = data_list[2].split(': ')[1]
samsha_data['Date Certified'] = data_list[3].split(': ')[1]
samsha_data['Waiver Count'] = data_list[4].split('for ')[1].split(' patients')[0]
print(samsha_data)