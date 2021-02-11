import pandas as pd

def clean_data(df):
    
df = pd.read_csv('data/2020.11.15-business-licences.csv', sep=';')

# %%
df.head()
# %%
df = df.loc[df['Province'] == 'BC']