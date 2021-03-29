# %%
import pandas as pd

from clean_data import identify_businesses


project_path = Path(__file__).parent.parent
data_path = project_path / 'data/2020.11.15-business-licences.csv'

# %%
df = identify_businesses(data_path)
# %%
df.head()
# %% [markdown]
# # Targets and features
#
# ## Targets
#
# - continuous (how long will business last?)
# - business lasts <= 1 year
# - business lasts <= 2 years
# - business lasts <= 3 years (it seems that the longer a business survives, the longer it is likely to survive, so I don't know how many of these year targets are worth looking at.)
#
# ## Features 
#
# - (done) number of revisions per year. May signal that owner is disorganized, etc. if they are not on top of their business license
# - more than one revision per year
# - discrete buckets of the various continuous measures (`NumberofEmployees`, `FeePaid`)
# - month, day of week of `IssuedDate`
# - inactive in year (dummy or count)
# - cancelled in year (dummy or count)
# - pending in year (dummy or count)
# - any combinations of the above
#
# I forgot that I did the cleanup such that each business has only one row per year. That means that I can't build the features that use within year-business variation. To make those features I need to either do so in the preprocessing or modify the preprocessing to not collapse the data to one observation per business per year. Ideally I would do the latter so I have a clean separation between preprocessing, feature building and splitting the data which minimizes the likelihood of data leakage.
# %%
df.columns
# %%
df['Status'].value_counts()
# %%
df['id'].unique().shape
# %%
df['BusinessType'].unique().shape
# %%

# revisions per year
(df.groupby('year_id')['id'].count() > 1).sum()

# %%
