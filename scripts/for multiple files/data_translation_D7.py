import os
import pandas as pd
from googletrans import Translator

# define the directory where the data files are located
data_dir = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 7'

# Iterate over each subfolder and look for the target file
for foldername in os.listdir(data_dir):
    folderpath = os.path.join(data_dir, foldername)
    if not os.path.isdir(folderpath):
        continue

    for filename in os.listdir(folderpath):
        basename, ext = os.path.splitext(filename)  # Separate the file base name and extension
        if basename.lower().endswith('beiräge') and ext == '.xlsx':  # Check if file base name ends with 'beiräge' (case-insensitive)
            filepath = os.path.join(folderpath, filename)
            if not os.path.isfile(filepath):
                continue

            translator = Translator()

            # Load the file into a pandas dataframe
            df_ger = pd.read_excel(filepath)

            # create new columns to store the translated comments
            df_ger['Titel (eng)'] = ''
            df_ger['Beschreibung (eng)'] = ''

            # loop over the columns you want to translate
            for col_name in ['Titel', 'Beschreibung']:
                # in order to send only one row at a time to google translator to remain within the character limit of google translator
                ### IT TAKES A LONG TIME IF THE DATASET IS BIG ###

                for i in range(len(df_ger[col_name])):
                    t = df_ger[col_name][i]
                    if pd.notnull(t):
                        try:
                            trans = translator.translate(t, src='de', dest='en')
                            if trans:
                                print(f"Translation: {trans.text}")
                                df_ger.loc[i, f'{col_name} (eng)'] = trans.text
                        except Exception as e:
                            print(f"Translation failed with error: {str(e)}")
                            continue

            # Save the updated dataframe to the same file name
            df_ger.to_excel(filepath, index=False)



