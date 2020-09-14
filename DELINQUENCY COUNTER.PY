import pandas as pd

# EDIT THESE TWO LINES BELOW TO POINT TO EXCEL SPREADSHEETS, THEN CLICK GREEN 'PLAY' BUTTON IN TOP-RIGHT CORNER
df       = pd.read_excel('C:/Users/Michael/Dropbox/Documents/!VILLAGE GREEN/Budget & Finance Committee/2020/08-Aug/delinquent.xlsx')
df_prior = pd.read_excel('C:/Users/Michael/Dropbox/Documents/!VILLAGE GREEN/Budget & Finance Committee/2020/07-Jul/delinquent.xlsx')

# determine accounts with largest decreases from prior month
current = df.groupby('account_id').sum()['balance']
prior = df_prior.groupby('account_id').sum()['balance']
top5 = current.subtract(prior, fill_value=0).sort_values()[0:5]
print('Accounts with largest decrease in total balance from prior month:')
print(top5)
print('')

# only keep rows pertaining to assessments
df = df[(df['trans_type']=='01 - Assessments') | (df['trans_type']=='02 - Special Assessment')]

# only keep necessary columns
df = df[['account_id','total30','total60','total90','total120','totalmore']]

# sum general and special assessments for each account
df = df.groupby('account_id').sum()

# only keep accounts with a delinquent balance greater than $10
df['balance'] = df['total30'] + df['total60'] + df['total90'] + df['total120'] + df['totalmore']
df = df.loc[df['balance']>10,:]

# calculate counts
count30 = sum(df['balance'] == df['total30'])
count60 = sum(df['balance'] == (df['total30'] + df['total60'])) - count30
count90 = sum(df['balance'] == (df['total30'] + df['total60'] + df['total90'])) - count30 - count60
count120 = sum(df['balance'] == (df['total30'] + df['total60'] + df['total90'] + df['total120'])) - count30 - count60 - count90
countmore = sum(df['balance'] == (df['total30'] + df['total60'] + df['total90'] + df['total120'] + df['totalmore'])) - count30 - count60 - count90 - count120
total = df['balance'].size

# generate output
if total == count30 + count60 + count90 + count120 + countmore:
    counts = {'<30 days':[count30], '30-120 days':[count60+count90+count120], '120+ days':[countmore], 'total':[total]}
    counts = pd.DataFrame(counts, columns=['<30 days','30-120 days','120+ days','total'])
    print('Number of unique accounts with delinquent assessments:')
    print(counts.to_string(index=False))    
else:
    print('CALCULATION EQUIVALENCE ERROR')

