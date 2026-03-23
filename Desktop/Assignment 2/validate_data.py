import pandas as pd
import numpy as np

df = pd.read_excel('Gaming Ballot Data Set-1.xls')

print('=== TARGET BALANCE ===')
vc = df['DEPENDENT VARIABLE'].value_counts()
print(vc)
print(f'Mean: {df["DEPENDENT VARIABLE"].mean():.4f}')

print('\n=== MSA UNIQUE VALUES ===')
print(df['MSA'].value_counts())

print('\n=== BALLOT TYPE UNIQUE VALUES ===')
print(df['BALLOT TYPE'].value_counts())

print('\n=== MISSING VALUES ALL COLS ===')
print(df.isnull().sum())

print('\n=== AGE REDUNDANCY CHECK ===')
age_diff = (df['NO OF OLDER'] - (df['AGE64'] + df['AGE OLDER THAN 65'])).abs().max()
younger_check = (df['NO OF YOUNGER'] - (df['AGE LESS THAN 18'] + df['AGE24'] + df['AGE44'])).abs().max()
print(f'NO OF OLDER vs AGE64+OLDER_65 max diff: {age_diff}')
print(f'NO OF YOUNGER vs age<18+24+44 max diff: {younger_check}')

minority_diff = (df['PERCENT MINORITY'] - (df['PERCENT BLACK'] + df['PERCENT OTHER'])).abs().max()
print(f'PERCENT MINORITY vs BLACK+OTHER diff: {minority_diff}')

female_diff = (df['PERCENT MALE'] + df['PERCENT FEMALE'] - 1).abs().max()
print(f'MALE + FEMALE sum to 1, diff: {female_diff}')

density_check = (df['POPULATION DENSITY'] - df['POPULATION'] / df['SIZE OF COUNTY']).abs().max()
print(f'POPULATION DENSITY vs POPULATION/SIZE diff: {density_check:.6f}')

print('\n=== AGE VARIABLE RANGES ===')
age_cols = ['AGE LESS THAN 18','AGE24','AGE44','AGE64','AGE OLDER THAN 65','NO OF OLDER','NO OF YOUNGER']
print(df[age_cols].describe())

print('\n=== SAMPLE DATA ===')
print(df[['DEPENDENT VARIABLE','FOR','AGAINST','BALLOT TYPE','MSA']].head(10))
