import warnings
import logging
import pandas as pd

logging.captureWarnings(True)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Call the last version of the dataframe
from b_data_translation import df_en

# Create an instance of the sentiment analyzer
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Define a function that takes a string and returns a dictionary of sentiment scores for that string
def get_sentiment_scores(text):
    scores = sia.polarity_scores(text)
    return scores

# Get sentiment scores for each row in the dataframe
sentiment_scores = []
for i in df_en['comment text']:
    sentiment_scores.append(get_sentiment_scores(i))

# Add the sentiment score results to the dataframe by only using the "compound" values
df_sent = pd.DataFrame(sentiment_scores)
compound_df = df_sent.loc[:, 'compound']

compound_list = compound_df.values.tolist() # put the values as a list to add into the dataframe
df_en['sentiment scores'] = compound_list # add the results as a new column

df_en.to_excel("x_final_data.xlsx", index=False)