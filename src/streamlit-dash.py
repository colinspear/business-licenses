from pathlib import Path

import numpy as np

import pandas as pd
import streamlit as st

# Set project path

project_path = Path.cwd()
df = pd.read_csv(project_path / 'data/2013-2021-clean.csv')
df['FOLDERYEAR'] = (df['FOLDERYEAR'] + 2000).astype('str')


st.title('Vancouver Business Churn')

status_count = df.groupby(['FOLDERYEAR', 'new_status'])['id'].count().unstack()
status_count = status_count.fillna(0)
status_count = status_count.astype('int')
status_count.columns = [s.lower() for s in status_count.columns]

active = status_count.loc[status_count.index==max(status_count.index), 'issued']
st.write(active.values)

st.line_chart(status_count)
