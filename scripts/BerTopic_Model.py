import matplotlib.pyplot as plt
from bertopic import BERTopic
from umap import UMAP
import numpy as np
import pandas as pd
import spacy
from sklearn.metrics.pairwise import cosine_similarity

# Function to get word vectors
def get_word_vector(word):
    return nlp(word).vector

# Function to calculate coherence of top words in a topic
def calculate_coherence(top_words):
    similarities = []
    for i in range(len(top_words)):
        for j in range(i + 1, len(top_words)):
            word_i = get_word_vector(top_words[i])
            word_j = get_word_vector(top_words[j])
            similarity = cosine_similarity(word_i.reshape(1, -1), word_j.reshape(1, -1))
            similarities.append(similarity[0][0])
    return np.mean(similarities)

# Function to calculate average coherence for a model
def calculate_average_coherence(topic_model, final_data):
    topics, _ = topic_model.fit_transform(final_data)
    topic_info = topic_model.get_topic_info()
    topic_coherence = {}
    for topic in topic_info['Topic'].unique():
        if topic == -1:  # Skip the outlier topic
            continue
        top_words = [word for word, _ in topic_model.get_topic(topic)]
        coherence_score = calculate_coherence(top_words)
        topic_coherence[topic] = coherence_score
    return np.mean(list(topic_coherence.values()))

# Load data
x = open("/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/intermediate_data/final_data_Elbchaussee.py", "r")
final_data = eval(x.readlines()[0])
x.close()

# Dataframe display settings
desired_width = 520
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# Convert to strings
final_data = [str(doc) for doc in final_data]
final_data = [doc for doc in final_data if doc != '[]']

# Initialize UMAP model
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)

# Load spaCy model for word embeddings
nlp = spacy.load("en_core_web_md")

# Initialize variables to store average coherence scores
average_coherence_scores = {}

# Loop over different numbers of topics
for num_topics in range(10, 24):  # 10 to 20 inclusive
    topic_model = BERTopic(nr_topics=num_topics, top_n_words=10, umap_model=umap_model, language="english", calculate_probabilities=True)
    avg_score = calculate_average_coherence(topic_model, final_data)
    average_coherence_scores[num_topics] = avg_score

# Create a DataFrame from the average coherence scores
df_coherence = pd.DataFrame(list(average_coherence_scores.items()), columns=['Number_of_Topics', 'Average_Coherence_Score'])

# Save the DataFrame to an Excel file
output_path = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/intermediate_data/average_coherence_scores.xlsx'
df_coherence.to_excel(output_path, index=False)
