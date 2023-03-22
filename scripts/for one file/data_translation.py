import pandas as pd
pd.options.mode.chained_assignment = None
from googletrans import Translator

translator = Translator()

### Import data from the excel file
df_ger = pd.read_excel('/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)/41. Magistrale Wandsbek/conceptioncomments_structured.xlsx')

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
df_ger.to_excel("/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)/41. Magistrale Wandsbek/conceptioncomments_structured.xlsx", index=False)

