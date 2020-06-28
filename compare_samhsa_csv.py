import pandas as pd
import os

path = os.getcwd()

df_og = pd.read_csv(path + '\\BupePrescribersData - allnames_June2020.csv', index_col=False)
df_1 = pd.read_csv(path + '\\Physician_Locator_06_23_2020_Phil-most-complete_515recs-after-removing-7-Philipsburg.csv', index_col=False)
df_2 = pd.read_csv(path + '\\Physician_Locator_06_27_2020.csv', index_col=False)

new_header = df_og.iloc[1] #grab the first row for the header
df_og = df_og[2:] #take the data less the header row
df_og.columns = new_header #set the header row as the df header

df_og = df_og[['First Name','Last Name']]
df_og = df_og.rename({'First Name': 'First', 'Last Name': 'Last'}, axis='columns')
# df_intersection_og_1 = pd.merge(df_og, df_1, how='inner', on=['First', 'Last'])
# df_intersection_og_1.dropna(inplace=True)
# df_intersection_og_1.reset_index(inplace=True)

df_diff_og_1 = df_1[(df_1.First.isin(df_og.First) == False) & (df_1.Last.isin(df_og.Last) == False)]
df_diff_og_1.to_csv(path + "\\06_23_minus_OG.csv", index=False)
df_diff_1_og = df_og[(df_og.First.isin(df_1.First) == False) & (df_og.Last.isin(df_1.Last) == False)]
df_diff_1_og.to_csv(path + "\\OG_minus_06_23.csv", index=False)
df_diff_og_2 = df_2[(df_2.First.isin(df_og.First) == False) & (df_2.Last.isin(df_og.Last) == False)]
df_diff_og_2.to_csv(path + "\\06_27_minus_OG.csv", index=False)
df_diff_2_og = df_og[(df_og.First.isin(df_2.First) == False) & (df_og.Last.isin(df_2.Last) == False)]
df_diff_2_og.to_csv(path + "\\OG_minus_06_27.csv", index=False)
# df_diff_og_1 = df_diff_og_1[df_diff_og_1.Last.isin(df_og.Last) == False]

print(df_diff_og_1)