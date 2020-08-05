import os
import pandas as pd

path = os.getcwd()
data_path = os.path.join(path, 'data', 'pals_final.csv')
final_df = pd.read_csv(data_path, index_col=False)


# Email
email = final_df[['FirstName', 'LastName', 'Emailid1']]

email = email.drop_duplicates()

email['count'] = email.groupby(['FirstName', 'LastName']).cumcount() + 1

email = email[email['count'] <= 5] # drop some of the Sarah Johnson results

email['colname'] = 'email' + email['count'].astype(str)

email = email.pivot(index = ['FirstName', 'LastName'], columns = 'colname', values = 'Emailid1')

# Zip
zipcode = final_df[['FirstName', 'LastName', 'zipcode']]

zipcode = zipcode.drop_duplicates()

zipcode['count'] = zipcode.groupby(['FirstName', 'LastName']).cumcount() + 1

zipcode = zipcode[zipcode['count'] <= 5]

zipcode['colname'] = 'zip' + zipcode['count'].astype(str)

zipcode = zipcode.pivot(index = ['FirstName', 'LastName'], columns = 'colname', values = 'zipcode')

# Effective Date
effect = final_df[['FirstName', 'LastName', 'StatusEffectivedate']]

effect = effect.drop_duplicates()

effect['count'] = effect.groupby(['FirstName', 'LastName']).cumcount() + 1

effect = effect[effect['count'] <= 5]

effect['colname'] = 'effectivedate' + effect['count'].astype(str)

effect = effect.pivot(index = ['FirstName', 'LastName'], columns = 'colname', values = 'StatusEffectivedate')

# Issue Date
issue = final_df[['FirstName', 'LastName', 'IssueDate']]

issue = issue.drop_duplicates()

issue['count'] = issue.groupby(['FirstName', 'LastName']).cumcount() + 1

issue = issue[issue['count'] <= 5]

issue['colname'] = 'issuedate' + issue['count'].astype(str)

issue = issue.pivot(index = ['FirstName', 'LastName'], columns = 'colname', values = 'IssueDate')

# Expiry Date
expiry = final_df[['FirstName', 'LastName', 'ExpiryDate']]

expiry = expiry.drop_duplicates()

expiry['count'] = expiry.groupby(['FirstName', 'LastName']).cumcount() + 1

expiry = expiry[expiry['count'] <= 5]

expiry['colname'] = 'expirydate' + expiry['count'].astype(str)

expiry = expiry.pivot(index = ['FirstName', 'LastName'], columns = 'colname', values = 'ExpiryDate')

# Renewal Date
renewal = final_df[['FirstName', 'LastName', 'LastRenewalDate']]

renewal = renewal.drop_duplicates()

renewal['count'] = renewal.groupby(['FirstName', 'LastName']).cumcount() + 1

renewal = renewal[renewal['count'] <= 5]

renewal['colname'] = 'lastrenewaldate' + renewal['count'].astype(str)

renewal = renewal.pivot(index = ['FirstName', 'LastName'], columns = 'colname', values = 'LastRenewalDate')

# Merge

merged = email.merge(zipcode, how='outer', left_index=True, right_index=True)

merged = merged.merge(effect, how='outer', left_index=True, right_index=True)

merged = merged.merge(issue, how='outer', left_index=True, right_index=True)

merged = merged.merge(expiry, how='outer', left_index=True, right_index=True)

merged = merged.merge(renewal, how='outer', left_index=True, right_index=True)

merged.to_csv('data/pals_wide.csv')