from pathlib import Path

import pandas as pd
import numpy as np

project_path = Path(__file__).parent.parent

df = pd.read_csv(project_path / 'data/2020.11.15-business-licences.csv', sep=';')

def identify_businesses(df):
    """Creates a unique identifier for each business in the data

    Args:
        df (pandas dataframe): historic business license data
    """
    # only interested in BC businesses
    df = df.loc[df['Province']=='BC']
    # may be able to drop this later
    df = df.loc[df['BusinessName'].notnull()]

    loc_cols = [
        'BusinessName', 'BusinessTradeName', 'BusinessType', 'BusinessSubType',
        'House', 'Street', 'City', 'PostalCode', 'LocalArea'
    ]

    # Any row with a NaN will be dropped when making id
    for col in loc_cols:
        df[col] = df[col].replace(np.nan, '')
        df[col] = df[col].replace('NaN', '')

    df['id'] = df.groupby(loc_cols).ngroup()
    df['year_id'] = df.groupby(loc_cols).ngroup()

    # If a license is revised in the same year, it will get another entry
    year_duplicates = df.loc[df['year_id'].duplicated(keep=False)]
    lic_revisions = year_duplicates.loc[~year_duplicates.duplicated(subset=['year_id', 'LicenceRevisionNumber'], keep=False)]
    lic_revisions['max_rev'] = lic_revisions.groupby('year_id')['LicenceRevisionNumber'].transform('max')
    lic_revisions.loc[lic_revisions['LicenceRevisionNumber']==lic_revisions['max_rev'], 'Status'].value_counts()
    lic_revisions_final = lic_revisions.loc[lic_revisions['LicenceRevisionNumber']==lic_revisions['max_rev']]

    # drop the initial subset of data and add back in the licencse revisions
    df = df.loc[~df['year_id'].isin(year_duplicates['year_id'])]
    df = df.append(lic_revisions_final.drop('max_rev', axis=1), verify_integrity=True)

    df['max_year'] = df.groupby('id')['FOLDERYEAR'].transform('max')
    df['min_year'] = df.groupby('id')['FOLDERYEAR'].transform('min')
    df['years_active'] = df['FOLDERYEAR'] - df['min_year']
    df['lifespan'] = df['max_year'] - df['min_year']
    
    # drop businesses begun in latest folder year
    df = df.loc[~((df['lifespan']==0) & (df['FOLDERYEAR']==df['max_year']))]

    # Many businesses do not notify the city when not renewing their license
    # Set business' last year to gone out of business
    df['new_status'] = df['Status']
    df.loc[df['max_year']==df['FOLDERYEAR'], 'new_status'] = 'GOB'

    # Drop businesses with entries after reportedly going out of business
    anomaly_id = df.loc[(df['new_status']=='Gone Out of Business') & (df['FOLDERYEAR']!=20), 'id'].unique()
    df = df.loc[~df['id'].isin(anomaly_id)]

    # Reclassify businesses cancelled or inactive in 2020 as gone out of business.
    df20 = df.loc[df['FOLDERYEAR']==df['max_year']]
    df = df.loc[df['FOLDERYEAR']!=df['max_year']]
    df20.loc[df20['Status'].isin(['Gone Out of Business', 'Cancelled', 'Inactive']), 'new_status'] = 'GOB'

    df = df.append(df20, verify_integrity=True)

    return df

identify_businesses(df)