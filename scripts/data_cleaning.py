import warnings
import logging

logging.captureWarnings(True)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import pandas as pd
import re

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import  WordNetLemmatizer
import nltk
import ssl

from gensim.models import TfidfModel
from gensim import corpora
import pickle
from collections import defaultdict
from gensim.models.phrases import Phrases

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Import Data From ConsulSUTD excel file -----------------------
def read_consul (fn = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 7/Elbchaussee/Elbchaussee Phase 1 Beiträge.xlsx'):
    df = pd.read_excel(fn, sheet_name='Sheet1', usecols= [26], header=0)
    return(df)

# CLEANING DATA ------------------------------------------------
# LOWERCASE ----------------------------------------------------
def make_lower (data):
    clean_text_1 = []
    for i in data.index:
        clean_text_1.append(str(data["Beschreibung (eng)"][i]).lower())
    return (clean_text_1)

# TOKENIZE SENTENCE --------------------------------------------
def sent_token (data):
    sent_tok = []
    for sent in data:
        sent = sent_tokenize(sent)
        sent_tok+=sent
    return (sent_tok)

def word_token (data):
    return ([word_tokenize(i) for i in data])

# PUNCTUATION
def remove_punc (list_punc):
    clean_biglist = []
    for words in list_punc:
        clean = []
        for w in words:
            res = re.sub(r'[^\w\s]', "", w)
            if res != "":
                clean.append(res)
        clean_biglist.append(clean)
    return clean_biglist

# SPECIAL CHARACTERS -------------------------------------------
def remove_char (list_punc):
    clean_char = []
    for words in list_punc:
        clean = []
        for item in words:
            l1 = item.removesuffix('_x000d_')
            if l1 != "":
                clean.append(l1)
        clean_char.append(clean)
    return clean_char

# STOPWORDS ----------------------------------------------------
def remove_stopword (list_stops):
    clean_biglist = []
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words.extend(['2','3','ti','it','1','due','behind','vice','versa',
                       'nt','also','us','one','could','would','till','le','el',
                       'among','eg','b','na','wan','pas','10','11','much',
                       'c','yes','no','ict','jie','4M','15M','5M','however',
                       'within','else','still','http','probably','may','us',
                       '4','_x000d_','sometimes','nu','15m','79','p','sth','8',
                       'even', 'nan','93','dtype','comment1','h', 'content_id',
                       'cpf', 'would', 'http', 'mani', ' ' ])
    for words in list_stops:
        w = []
        for word in words:
            if not word in stop_words:
                w.append(word)
        clean_biglist.append(w)
    return clean_biglist

# STEMMING -----------------------------------------------------
def stem_text (list_stem):
    porter = PorterStemmer()
    stem_biglist = []
    for words in list_stem:
        w = []
        for word in words:
            w.append(porter.stem(word))
        stem_biglist.append(w)
    return stem_biglist

# LEMITIZATION -------------------------------------------------

def lemit_text (list_lemit):
    wnet = WordNetLemmatizer()
    lemit_biglist = []
    for words in list_lemit:
        w = []
        for word in words:
            w.append(wnet.lemmatize(word))
        lemit_biglist.append(w)
    return lemit_biglist

# Remove less frequent words -------------------------------------------------
def remove_less_frequent_words(texts, cutoff_value):
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    clean_texts = [[token for token in text if frequency[token] > cutoff_value] for text in texts]
    return clean_texts

# Call Functions -----------------------------------------------
df = read_consul()
clean_text_1 = make_lower(df)
clean_text_2 = sent_token(clean_text_1)
clean_text_3 = word_token(clean_text_2)
clean_text_4 = remove_punc(clean_text_3)
clean_text_5 = remove_stopword(clean_text_4)
clean_text_6 = remove_char(clean_text_5)
clean_text_7 = lemit_text(clean_text_5)
clean_text_8 = stem_text(clean_text_6)
clean_text_9 = remove_less_frequent_words(clean_text_7, 10)

# CREATE BIGRAMS AND TRIGRAMS ----------------------------------------
bigram = Phrases(clean_text_9, min_count=10, threshold=50)
trigram = Phrases(bigram[clean_text_9],min_count=10, threshold=50)

clean_text_10 = trigram[bigram[clean_text_9]]
clean_text_11 = list(clean_text_10)

print(clean_text_11)

# FINAL DATA ----------------------------------------
final_data = clean_text_11
# print(final_data)


# TF-IDF REMOVAL -----------------------------------------
# Convert final_data to a dictionary of term-frequency pairs
id2word = corpora.Dictionary(final_data)
# Convert each document in final_data to a bag-of-words representation
# (i.e. a list of tuples, where each tuple represents a term and its frequency)
corpus = [id2word.doc2bow(text) for text in final_data]

# Train a TF-IDF model on the corpus
tfidf = TfidfModel(corpus, id2word=id2word)

low_value = 0.03
words = []
words_missing_in_tfidf = []

# Iterate over each document in the corpus
for i in range(0, len(corpus)):
    bow = corpus[i]
    low_value_words = []  # Reinitialize to be safe. You can skip this.
    tfidf_ids = [id for id, value in tfidf[bow]]
    bow_ids = [id for id, value in bow]

    # Find words with low TF-IDF score
    low_value_words = [id for id, value in tfidf[bow] if value < low_value]
    # Find words that were dropped in previous iterations
    drops = low_value_words + words_missing_in_tfidf

    # Add the dropped words to a list
    for item in drops:
        words.append(id2word[item])

    # Find words that are missing from the current document due to their low TF-IDF score
    words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids]

    # Create a new bag-of-words representation that excludes the low-value and missing words
    new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]
    # Replace the original document in the corpus with the new bag-of-words representation
    corpus[i] = new_bow

# TF-IDF REMOVAL -----------------------------------------
# save the final corpus
with open('/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/intermediate_data/corpus_Elbchaussee.pkl', 'wb') as f:
    pickle.dump(corpus, f)

x = open("/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/intermediate_data/final_data_Elbchaussee.py", "w+")
x.write(str(final_data))
x.close()
