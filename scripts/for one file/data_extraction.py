import warnings
import logging
logging.captureWarnings(True)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd
import numpy as np
import copy
import os

### Dataframe display settings
desired_width=520
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)


### THIS CODE IS FOR DATA EXTRACTION FROM ONE FILE ###
# Define the directory path as a variable
dir_path = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)/XXX'

# Import data from the Excel file
df = pd.read_excel(os.path.join(dir_path, 'conceptioncomments.xlsx'))

# Modify column names to make it more readable
df.rename(columns={'Contribution ID': 'topic', 'Comment ID': 'reply', 'Comment Subject': 'comment', 'Comment Text': 'comment text','created (UTC)': 'timestamp'}, inplace=True)

# Modify topic and comment names in columns
df['topic'] = 'topic ' + df['topic'].astype(str)
df["comment"] = df["comment"].str.split().str[-1]

# Turn the strings into integers in the comment column
for i, value in enumerate(df["comment"]):
    if isinstance(value, str):
        df.at[i, "comment"] = int(value)

#### CREATING A DATAFRAME WITH PARENT AND CHILD COLUMNS ####
new_df = pd.DataFrame()
unique_values = []

include_replies = True # include lines with replies by default

for i in range(len(df.iloc[:,0])):

    # take the topic numbers as unique values
    if df['topic'].to_list()[i] not in unique_values:
        unique_values.append(df['topic'].to_list()[i])

    # filter out the comments with no replies and turn each row to an object with the information under columns
    if include_replies or df['reply'].to_list()[i] in df['comment'].to_list() or (str(df['comment'].to_list()[i]) != " " and str(df['comment'].to_list()[i]) != "nan"):
        row = df.iloc[i,:]

        #turn each row into a dictionary (column names: keys, rows: values)
        new_row = copy.deepcopy(row)
        new_dict = new_row.to_dict()

        #locate topic numbers as parents under root
        if str(row['comment']) == "nan":
            new_dict.update({'comment': row['topic']})

        new_df = new_df.append(new_dict, ignore_index=True)

### Add the unique values (topics) as children into the dataframe
for val in unique_values:
    new_row = copy.deepcopy(new_df.iloc[0,:])
    new_dict = new_row.to_dict()
    for x,y in new_dict.items():
        if x == 'reply':
            new_dict.update({'reply':val})
        else: new_dict.update({x:''})
    new_df = new_df.append(new_dict, ignore_index=True)
    new_df['comment'].replace('', ' ', inplace=True)
    new_df.dropna(subset=['comment'], inplace=True)

# Save the new dataframe to an Excel file in the same directory
new_df.to_excel(os.path.join(dir_path, 'conceptioncomments_structured.xlsx'), index=False)