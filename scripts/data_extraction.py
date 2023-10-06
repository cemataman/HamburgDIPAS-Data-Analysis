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
dir_path = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)/41. Magistrale Wandsbek'

# Import data from the Excel file
df = pd.read_excel(os.path.join(dir_path, 'conceptioncomments.xlsx'))

# Modify column names to make it more readable
df.rename(columns={'Contribution ID': 'topic',
                   'Comment ID': 'reply',
                   'Comment Subject': 'comment',
                   'Comment Text': 'comment text',
                   'created (UTC)': 'timestamp'},
          inplace=True)

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

### Set the timestamps

df_time = new_df

# define a custom function to apply to each row
def get_timestamp(row):
    if row['comment'] in df['reply'].values:
        reply_timestamp = df.loc[df['reply'] == row['comment'], 'timestamp'].iloc[0]
        return reply_timestamp

# create a new column with timestamp values
df_time['timestamp_comment'] = df_time.apply(get_timestamp, axis=1)

# Check if "xx" is empty and fill it with the value from "timestamp" column in the same row
df_time['timestamp_comment'] = df_time['timestamp_comment'].fillna(df_time['timestamp'])

# convert timestamp columns to datetime format and remove timezone information
df_time['timestamp'] = pd.to_datetime(df_time['timestamp']).dt.tz_localize(None)
df_time['timestamp_comment'] = pd.to_datetime(df_time['timestamp_comment']).dt.tz_localize(None)

# calculate time difference in minutes
df_time['time_difference_min'] = ((df_time['timestamp'] - df_time['timestamp_comment']) / pd.Timedelta(minutes=1))

# calculate time difference in minutes
df_time['time_difference_hr'] = ((df_time['timestamp'] - df_time['timestamp_comment']) / pd.Timedelta(hours=1))


#### NORMALIZE THE VALUES  -------------------------------------------------------------------------
# select the column to normalize
column_to_normalize = "time_difference_hr"

### Choose a scaling method
# calculate the normalized values using Min-Max scaling
min_value = df_time[column_to_normalize].min()
max_value = df_time[column_to_normalize].max()
df_time["normalized_column"] = (df_time[column_to_normalize] - min_value) / (max_value - min_value)

# # or, calculate the normalized values using Z-score scaling
# mean_value = df_time[column_to_normalize].mean()
# std_value = df_time[column_to_normalize].std()
# df_time["normalized_column"] = (df_time[column_to_normalize] - mean_value) / std_value

# calculate the mean of the values column without including zero values
mean = df_time.loc[df_time['normalized_column'] != 0, 'normalized_column'].mean()

# replace all 0 values in column 'normalized_column' with 1 --> this is for visualization purposes
df_time['normalized_column'] = df_time['normalized_column'].replace(0, 1)


# Count the number of letters in each cell of 'comment text (eng)' column
# and save it in a new column named 'Length'
df_time['Length'] = df_time['comment text'].str.len()

# If 'Length' is empty or 0, put 100 instead
df_time['Length'].fillna(100, inplace=True)  # Fill NaN values with 100
df_time['Length'].replace(0, 100, inplace=True)  # Replace 0 values with 100

# Step 3: Find the maximum value in the 'Length' column
max_length = df_time['Length'].max()

# Step 4: Apply scaled logarithmic normalization
df_time['normalized_length'] = (10 * np.log(df_time['Length'])) / np.log(max_length)

# Save the new dataframe to an Excel file in the same directory
df_time.to_excel(os.path.join(dir_path, 'deneme.xlsx'), index=False)