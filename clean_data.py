import pandas as pd
import numpy as np

def clean_data(df):
    # drop cancelled applications (df['Status']=='Cancelled')