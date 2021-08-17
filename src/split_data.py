# %%
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from clean_data import identify_businesses


project_path = Path(__file__).parent.parent
data_path = project_path / 'data/2020.11.15-business-licences.csv'

df = identify_businesses(data_path)
# %% [markdown]
# # Targets and features

# ## Targets

# - continuous (how long will business last?)
# - business lasts <= 1 year
# - business lasts <= 2 years
# - business lasts <= 3 years (it seems that the longer a business survives, the longer it is likely to survive, so I don't know how many of these year targets are worth looking at.)

# ## Features 

# - (TODO) Requires within year variation
#   - (done) number of revisions per year. May signal that owner is disorganized, etc. if they are not on top of their business license
#   - more than one revision per year
#   - inactive in year (dummy or count)
#   - cancelled in year (dummy or count)
#   - pending in year (dummy or count)
# - Doesn't require within year variation
#   - Continuous variables. If used as continuous variables will likely need some transformation: normalization, rescale, etc. I can also try turning them into discrete variables by bucketing
#       - `NumberofEmployees` 
#       - `FeePaid`
#       - discrete buckets of the various continuous measures (`NumberofEmployees`, `FeePaid`)
#   - Categorical variables
#       - `UnitType`
#       - `LocalArea`
#       - `BusinessType`
#       - `BusinessSubType`
#       - `Street` (could possibly use to interpolate `LocalArea` where missing)
#   - month, day of week of `IssuedDate`

# %%
df.columns
# %%
# inspect unit, unit type, business type and subtype

vars = ['Unit', 'UnitType', 'LocalArea', 'FeePaid', 
    'BusinessType', 'BusinessSubType', 'Street', 'House']

for v in vars:
    print(v, '\n', df[v].describe(), '\n')

# %% [markdown]
# **Cleaning notes**

# - `Unit` is number, probably not useful, could extract floor maybe?
# - `UnitType` is mostly non-descriptive (`UnitType=='Unit'`), could provide togle in case it's useful for the other categories
# - `LocalArea` (neighborhood) looks good, some missing values, but mostly not. Clean
# - `FeePaid` has some variation, but I'm not sure what it's value could be. Maybe normalize and 



# %%

# one hot encode population, neighborhood, business type / subtype
bins = [0, 2, 6, 11, 21, 51, 101, 201, df['NumberofEmployees'].max()]
empl_bins = pd.cut(df['NumberofEmployees'], bins, right=False)

enc = OneHotEncoder(handle_unknown='ignore')
enc.fit(empl_bins)
# %%
df.loc[df['NumberofEmployees']>=5000, ['NumberofEmployees', 'BusinessName']]

# %%
df['BusinessType'].unique().shape
# %%

# revisions per year
(df.groupby('year_id')['id'].count() > 1).sum()

# %%

# There are a number of categorical variables we can one hot encode

