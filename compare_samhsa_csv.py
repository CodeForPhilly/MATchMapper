import pandas as pd
import os

class SAMHSA_Entry:

    def __init__(self, name_prefix, first_name, last_name, address, address_complement, city, county, state, postal_code, telephone, fax):
        self.name_prefix = str(name_prefix)
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.address = str(address)
        self.address_complement = str(address_complement)
        self.city = str(city)
        self.county = str(county)
        self.state = str(state)
        self.postal_code = str(postal_code)
        self.telephone = str(telephone)
        self.fax = str(fax)

     # OVERRIDE
    def __str__(self):
        return str("name_prefix: %s, first_name: %s, last_name: %s, address: %s, address_complement: %s, city: %s, county: %s, state: %s, postal_code: %s, telephone: %s, fax: %s" \
        %(self.name_prefix, self.first_name, self.last_name, self.address, self.address_complement, self.city \
        , self.county, self.state, self.postal_code, self.telephone, self.fax))

    def __eq__(self, other):
        if isinstance(other, SAMHSA_Entry):
            return self.name_prefix == other.name_prefix and self.first_name == other.first_name and self.last_name == other.last_name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name_prefix + ' ' + self.first_name + ' ' + self.last_name + ' ' + self.address + ' ' +  \
        self.address_complement + ' ' + self.city + ' ' + self.county + ' ' + self.state + ' ' + self.postal_code \
         + ' ' + self.telephone + ' ' + self.fax)


path = os.getcwd()

df_1 = pd.read_csv(os.path.join(path, 'samhsa_comparison_data', 'BPLocator_2020-05-07_472recs-for-Philadelphia.csv'), index_col=False)
df_2 = pd.read_csv(os.path.join(path, 'samhsa_comparison_data', 'BPLocator_2020-06-15_Philadelphia_505recs.csv'), index_col=False)

df_1_set = set()
df_2_set = set()

for index, rows, in df_1.iterrows():
    df_1_set.add(SAMHSA_Entry(rows['name_prefix'], rows['First'], rows['Last'], rows['Address'], rows['Address Complement'] \
    , rows['City'], rows['County'], rows['State'], rows['Postal Code'], rows['Telephone'], rows['Fax']))

for index, rows, in df_2.iterrows():
    df_2_set.add(SAMHSA_Entry(rows['name_prefix'], rows['First'], rows['Last'], rows['Address'], rows['Address Complement'] \
    , rows['City'], rows['County'], rows['State'], rows['Postal Code'], rows['Telephone'], rows['Fax']))

removed_or_edited = df_1_set - df_2_set
edited_or_added = df_2_set - df_1_set

removed = set()
edited = set()
added = set()

for entry in removed_or_edited:
    matched = False
    for new_entry in edited_or_added:
        if entry == new_entry:
            edited.add(new_entry)
            matched = True
    if not matched:
        removed.add(entry)

for new_entry in edited_or_added:
    matched = False
    for entry in removed_or_edited:
        if new_entry == entry:
            matched = True
            break
    if not matched:
        added.add(new_entry)


print([str(x) for x in removed], len([str(x) for x in removed]))
print()
print([str(x) for x in edited], len([str(x) for x in edited]))
print()
print([str(x) for x in added], len([str(x) for x in added]))