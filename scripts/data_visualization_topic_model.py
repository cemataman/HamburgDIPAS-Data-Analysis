import matplotlib
import matplotlib.pyplot as plt
from bertopic import BERTopic
from umap import UMAP
import os
import pandas as pd
import numpy as np
import plotly.io as py

# Load data
x = open("/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/intermediate_data/final_data_Elbchaussee.py", "r")
final_data = eval(x.readlines()[0])
x.close()

### Dataframe display settings
desired_width = 520
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# Set the background color to white
matplotlib.rcParams['figure.facecolor'] = 'white'

# Convert non-string elements to strings in the corpus
final_data = [str(doc) for doc in final_data]

# Filter out the empty lists:
final_data = [doc for doc in final_data if doc != '[]']

# Initiate UMAP
umap_model = UMAP(n_neighbors=15,
                  n_components=5,
                  min_dist=0.0,
                  metric='cosine',
                  random_state=42)


# Initiate BERTopic
topic_model = BERTopic(nr_topics=18, top_n_words=10, umap_model=umap_model, language="english", calculate_probabilities=True)

# Run BERTopic model
topics, probabilities = topic_model.fit_transform(final_data)

# Get topic information
topic_info = topic_model.get_topic_info()
print(topic_info)

# Get specific topic information
topic_info_n = topic_model.get_topic(2)
print(topic_info_n)

# Convert the topic_info DataFrame to have the desired columns
topic_df = pd.DataFrame(topic_info, columns=['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs'])

# Save to Excel
excel_path = "/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/intermediate_data/topic_model_results_Elbchaussee.xlsx"
topic_df.to_excel(excel_path, index=False)


# # Generate the plot for TOPIC BARCHART
# plot_figure = topic_model.visualize_barchart(top_n_topics=18)
# py.write_html(plot_figure, '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/results/visuals/topic_barchart.html') # Save to an HTML file

# # Generate the plot for TOPIC HIERARCHY
# plot_figure_2 = topic_model.visualize_hierarchy()
# plot_figure_2.update_layout(plot_bgcolor='white')
# py.write_html(plot_figure_2, '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/results/visuals/topic_hierarchy.html') # Save to an HTML file
#
# # Generate the plot for TOPIC SIMILARITY
# plot_figure_3 = topic_model.visualize_heatmap()
# py.write_html(plot_figure_3, '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/results/visuals/topic_similarity.html') # Save to an HTML file
#
# # Generate the plot for INTERTOPIC DISTANCE MAP
# plot_figure_4 = topic_model.visualize_topics()
# py.write_html(plot_figure_4, '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/results/visuals/intertopic_distance_map.html') # Save to an HTML file
