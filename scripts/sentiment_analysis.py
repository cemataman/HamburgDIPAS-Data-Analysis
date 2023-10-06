import warnings
import logging
import pandas as pd
from textblob import TextBlob

logging.captureWarnings(True)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

### Import data from the excel file
# Define the directory path as a variable
dir_path = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)/41. Magistrale Wandsbek/deneme.xlsx'
df_en = pd.read_excel(dir_path)


# Create an instance of the sentiment analyzer
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Define functions that takes a string and returns a dictionary of sentiment scores for that string --> different libraries for different functions
def get_sentiment_scores_sia(text):
    scores = sia.polarity_scores(text)
    return scores

def get_sentiment_scores_blob(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Get sentiment scores for each row in the dataframe
sentiment_scores = []
for i in df_en['comment text (eng)']:
    if isinstance(i, float):  # check if the value is a float
        i = str(i)  # convert float to string
    sentiment_scores.append(get_sentiment_scores_sia(i))

# Add the sentiment score results to the dataframe by only using the "compound" values
df_sent = pd.DataFrame(sentiment_scores)
compound_df = df_sent.loc[:, 'compound']

compound_list = compound_df.values.tolist() # put the values as a list to add into the dataframe
df_en['sentiment scores'] = compound_list # add the results as a new column

df_en.to_excel(dir_path, index=False)