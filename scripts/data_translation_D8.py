import pandas as pd
pd.options.mode.chained_assignment = None
from googletrans import Translator

translator = Translator()

### Import data from the excel file
# Define the directory path as a variable
dir_path = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)/xx. Stadteingang Elbbruecken/conceptioncomments_structured.xlsx'
df_ger = pd.read_excel(dir_path)

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
                df_ger['comment text (eng)'][i] = trans.text
        except Exception as e:
            print(str(e))
            continue

### save the translated data as an excel file
df_ger.to_excel(dir_path, index=False)

