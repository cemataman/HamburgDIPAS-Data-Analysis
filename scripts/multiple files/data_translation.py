import os
import pandas as pd
from googletrans import Translator

# define the directory where the data files are located
data_dir = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)'

# Iterate over each subfolder and look for the target file
for foldername in os.listdir(data_dir):
    folderpath = os.path.join(data_dir, foldername)
    if not os.path.isdir(folderpath):
        continue
    filepath = os.path.join(folderpath, 'conceptioncomments_structured.xlsx')
    if not os.path.isfile(filepath):
        continue

    translator = Translator()

    # Load the file into a pandas dataframe
    df_ger = pd.read_excel(filepath)

    # create a new column to store the translated comments
    df_ger['comment text (eng)'] = ''

    # in order to send only one row at a time to google translator to remain within the character limit of google translator
    ### IT TAKES A LONG TIME IF THE DATASET IS BIG ###

    for i in range(len(df_ger['comment text'])):
        t = df_ger['comment text'][i]
        if pd.notnull(t):  # skip null or NaN values
            try:
                trans = translator.translate(t, src='de', dest='en')
                if trans:
                    df_ger.loc[i, 'comment text (eng)'] = trans.text
            except Exception as e:
                print(str(e))
                continue

    # Save the updated dataframe to the same file name
    df_ger.to_excel(filepath, index=False)
