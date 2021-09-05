from pathlib import Path

import numpy as np

import pandas as pd
import streamlit as st

# Set project path

project_path = Path.cwd()
df = pd.read_csv(project_path / 'data/2013-2021-clean.csv')
df['FOLDERYEAR'] = (df['FOLDERYEAR'] + 2000).astype('str')


st.title('Vancouver Business License Dashboard')

# count businesses by license status
status_count = df.groupby(['FOLDERYEAR', 'new_status'])['id'].count().unstack()
status_count = status_count.fillna(0)
status_count = status_count.astype('int')
status_count.columns = [s.lower() for s in status_count.columns]

# number of currently active businesses
active = status_count.iloc[-1]['issued']
st.write(active)

# number of new businesses this year
max_year = max(set(df['FOLDERYEAR']))
y = set(df.loc[df['FOLDERYEAR'] == max_year, 'id'].unique())
y_1 = set(df.loc[df['FOLDERYEAR'] == str(int(max_year)-1), 'id'].unique())
st.write(len(y - y_1))


st.line_chart(status_count)
