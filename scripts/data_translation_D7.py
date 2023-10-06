import pandas as pd
pd.options.mode.chained_assignment = None
from googletrans import Translator

translator = Translator()

# Define the file path
file_path = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 7/Eimsbüttel 2040/Eimsbüttel 2040 Phase 1 Beiträge.xlsx'

### Import data from the excel file
df_ger = pd.read_excel(file_path)

# create new columns to store the translated comments
df_ger['Titel (eng)'] = ''
df_ger['Beschreibung (eng)'] = ''
df_ger['dates'] = ''

# Remove duplicate rows in the "Beschreibung" column
df_ger.drop_duplicates(subset='Beschreibung', inplace=True)

# reset the index of the DataFrame
df_ger.reset_index(drop=True, inplace=True)

# in order to send only one row at a time to google translator to remain within the character limit of google translator
### IT TAKES A LONG TIME IF THE DATASET IS BIG ###

for i in range(len(df_ger['Titel'])):
    t = df_ger['Titel'][i]
    if pd.notnull(t):  # skip null or NaN values
        try:
            trans = translator.translate(t, src='de', dest='en')
            if trans:
                df_ger['Titel (eng)'][i] = trans.text
        except Exception as e:
            print(str(e))
            continue

    t2 = df_ger['Beschreibung'][i]
    if pd.notnull(t2):  # skip null or NaN values
        try:
            trans2 = translator.translate(t2, src='de', dest='en')
            if trans2:
                df_ger['Beschreibung (eng)'][i] = trans2.text
        except Exception as e:
            print(str(e))
            continue

    t3 = df_ger['Veroffentlicht'][i]
    if pd.notnull(t3):  # skip null or NaN values
        try:
            trans3 = translator.translate(t3, src='de', dest='en')
            if trans3:
                df_ger['dates'][i] = trans3.text
        except Exception as e:
            print(str(e))
            continue

### save the translated data as an excel file
df_ger.to_excel(file_path, index=False)
