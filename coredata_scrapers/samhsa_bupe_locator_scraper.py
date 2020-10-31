import requests
import lxml.html as lh
import pandas as pd
import math
import os
from datetime import datetime

now = datetime.today().strftime('%Y-%m-%d')

has_page = True
page_index = 0
bupe_locator_data = []

while has_page:
    url = 'https://www.samhsa.gov/medication-assisted-treatment/practitioner-program-data/treatment-practitioner-locator/results/_none/10/Phila/PA?page=' + str(page_index)
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    if len(tr_elements) == 0:
        break
    headers = ['name_prefix']
    for column_name in tr_elements[0]:
        headers.append(column_name.text_content())
    del headers[1]
    for i in range(len(tr_elements) - 1):
        bupe_provider = dict()
        key_counter = 0
        for t in tr_elements[i + 1]:
            item = t.text_content()
            bupe_provider[headers[key_counter]] = item.strip()
            key_counter += 1
        bupe_locator_data.append(bupe_provider)
    page_index += 1

final_df = pd.DataFrame(bupe_locator_data) 
file_name = "samhsa_bupe_locator_" + now + ".csv" 
final_df.to_csv(os.path.join(os.getcwd(), "data", file_name), index=False)
