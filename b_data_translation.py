import pandas as pd
pd.options.mode.chained_assignment = None
from googletrans import Translator
from a_data_extraction import new_df

translator = Translator()

# call the selected comments into a dataframe
df_ger = new_df.iloc[:,[3]]

# in order to send only one row at a time to google translator to remain within the character limit of google translator
### IT TAKES A LONG TIME IF THE DATASET IS BIG ###
for i in range(len(df_ger['comment text'])):
    t = df_ger['comment text'][i]
    if t:
        try:
            trans = translator.translate(t, src='de', dest='en')
            if trans:
                df_ger['comment text'][i] = trans.text
        except Exception as e:
            print(str(e))
            continue
new_df["comment text"] = df_ger
df_en = new_df

# save the translated data as an excel file
# df.to_excel("data_en.xlsx", index=False)

