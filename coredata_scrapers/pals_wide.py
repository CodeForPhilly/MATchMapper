import os
import pandas as pd
from datetime import date

path = os.getcwd()
##TODO: Change input filename below to match whichever installment you're checking
data_path = os.path.join(path, 'data', 'PALS_tall_2020-09-23_528_.csv')
final_df = pd.read_csv(data_path, index_col=False)

# emails
email = final_df[['FirstName', 'LastName', 'Emailid1']]
email = email.drop_duplicates()
email = email.sort_values(['LastName', 'FirstName', 'Emailid1'], ascending=[True, True, False])
email['count'] = email.groupby(['FirstName', 'LastName']).cumcount() + 1
email['colname'] = 'email' + email['count'].astype(str)
email = email.pivot(index = ['FirstName', 'LastName'], columns = 'colname', values = 'Emailid1')
email.reset_index(inplace = True)

# Zip
zipcode = final_df[['FirstName', 'LastName', 'zipcode']]
zipcode = zipcode.drop_duplicates()
zipcode = zipcode.sort_values(['LastName', 'FirstName', 'zipcode'], ascending = [True, True, False])
zipcode['count'] = zipcode.groupby(['FirstName', 'LastName']).cumcount() + 1
zipcode = zipcode[zipcode['count'] <= 4]
zipcode['colname'] = 'zip' + zipcode['count'].astype(str)
zipcode = zipcode.pivot(index = ['FirstName', 'LastName'], columns = 'colname', values = 'zipcode')
zipcode.reset_index(inplace = True)

# Status Effective
effect = final_df[['FirstName', 'LastName', 'StatusEffectivedate']]
effect = effect.drop_duplicates()
effect['StatusEffectivedate'] = pd.to_datetime(effect['StatusEffectivedate'])
effect = effect.groupby(['FirstName', 'LastName'])['StatusEffectivedate'].agg(['min', 'max']).rename(columns={'min': 'oldest_StatusEffectivedate', 'max': 'newest_StatusEffectivedate'})
effect['newest_StatusEffectivedate']= effect['newest_StatusEffectivedate'].dt.strftime('%Y-%m-%d')
effect['oldest_StatusEffectivedate']= effect['oldest_StatusEffectivedate'].dt.strftime('%Y-%m-%d')
effect.reset_index(inplace = True)

# Issue Date
issue = final_df[['FirstName', 'LastName', 'IssueDate']]
issue = issue.drop_duplicates()
issue['IssueDate'] = pd.to_datetime(issue['IssueDate'])
issue = issue.groupby(['FirstName', 'LastName'])['IssueDate'].agg(['min', 'max']).rename(columns={'min': 'oldest_IssueDate', 'max': 'newest_IssueDate'})
issue['newest_IssueDate']= issue['newest_IssueDate'].dt.strftime('%Y-%m-%d')
issue['oldest_IssueDate']= issue['oldest_IssueDate'].dt.strftime('%Y-%m-%d')
issue.reset_index(inplace = True)

# Expiry Date
expiry = final_df[['FirstName', 'LastName', 'ExpiryDate']]
expiry = expiry.drop_duplicates()
expiry['ExpiryDate'] = pd.to_datetime(expiry['ExpiryDate'])
expiry = expiry.groupby(['FirstName', 'LastName'])['ExpiryDate'].agg(['min', 'max']).rename(columns={'min': 'oldest_ExpiryDate', 'max': 'newest_ExpiryDate'})
expiry['newest_ExpiryDate']= expiry['newest_ExpiryDate'].dt.strftime('%Y-%m-%d')
expiry['oldest_ExpiryDate']= expiry['oldest_ExpiryDate'].dt.strftime('%Y-%m-%d')
expiry.reset_index(inplace = True)

# renewal Date
renewal = final_df[['FirstName', 'LastName', 'LastRenewalDate']]
renewal = renewal.drop_duplicates()
renewal['LastRenewalDate'] = pd.to_datetime(renewal['LastRenewalDate'])
renewal = renewal.groupby(['FirstName', 'LastName']).agg(LastRenewalDate = pd.NamedAgg(column = 'LastRenewalDate', aggfunc = 'max'))
renewal['LastRenewalDate']= renewal['LastRenewalDate'].dt.strftime('%Y-%m-%d')
renewal.reset_index(inplace = True)

# write
merged = email.merge(zipcode, how='outer', left_index=True, right_index=True, on = ['FirstName', 'LastName'])
merged = merged.merge(effect, how='outer', left_index=True, right_index=True, on = ['FirstName', 'LastName'])
merged = merged.merge(issue, how='outer', left_index=True, right_index=True, on = ['FirstName', 'LastName'])
merged = merged.merge(expiry, how='outer', left_index=True, right_index=True, on = ['FirstName', 'LastName'])
merged = merged.merge(renewal, how='outer', left_index=True, right_index=True, on = ['FirstName', 'LastName'])

outdate = date.today().strftime('%Y-%m-%d')
outlen = merged.shape[0]

merged.to_csv(os.path.join(path, 'data', f"PALS_wide_{outdate}_{outlen}_.csv"), index=False)