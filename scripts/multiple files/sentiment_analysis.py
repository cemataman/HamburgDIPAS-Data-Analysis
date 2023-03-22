import os
import warnings
import logging
import pandas as pd
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

logging.captureWarnings(True)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Define functions that takes a string and returns a dictionary of sentiment scores for that string --> different libraries for different functions
def get_sentiment_scores_sia(text):
    scores = sia.polarity_scores(text)
    return scores

def get_sentiment_scores_blob(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

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

    sia = SentimentIntensityAnalyzer()

    # Load the file into a pandas dataframe
    df_en = pd.read_excel(filepath)

    # Get sentiment scores for each row in the dataframe
    sentiment_scores = []
    for i in df_en['comment text (eng)']:
        if isinstance(i, float):  # check if the value is a float
            i = str(i)  # convert float to string
        sentiment_scores.append(get_sentiment_scores_sia(i))

    # Add the sentiment score results to the dataframe by only using the "compound" values
    df_sent = pd.DataFrame(sentiment_scores)
    compound_df = df_sent.loc[:, 'compound']

    compound_list = compound_df.values.tolist()  # put the values as a list to add into the dataframe
    df_en['sentiment scores'] = compound_list  # add the results as a new column

    # Save the updated dataframe to the same file name
    df_en.to_excel(filepath, index=False)
