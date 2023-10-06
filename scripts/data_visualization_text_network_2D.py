import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import numpy as np
import os
import plotly.io as pio

path = '/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)/43. Spielplatz bei der Osterkirche/conceptioncomments_structured.xlsx'

# get the folder name where the Excel file is saved
folder_name = os.path.basename(os.path.dirname(path))

# read nodes from Excel file
df = pd.read_excel(path, usecols=['topic', 'comment', 'reply', 'sentiment scores', 'comment text (eng)', 'normalized_column', 'normalized_length'])

# Display unique topic names
unique_topics = df['topic'].dropna().unique()
print("Topic names:")
for topic in unique_topics:
    print(topic)

# Filter the DataFrame based on user input
topic_name = input("Enter the topic name or 'all' for all topics: ")
if topic_name.lower() != "all":
    df = df[df['topic'] == topic_name]

# replace empty spaces with NaN values
df['comment'] = df['comment'].replace(' ', np.nan)

# drop rows with NaN values
df.dropna(subset=['comment'], inplace=True)

node_names = list(set(df['comment'].tolist() + df['reply'].tolist()))

# initialize node colors to grey
node_colors = ['grey'] * len(node_names)

# set node colors based on sentiment score
for i, row in df.iterrows():
    comment = row['comment']
    reply = row['reply']
    sentiment_score = row['sentiment scores']
    if reply in node_names:
        node_colors[node_names.index(reply)] = sentiment_score

# create graph
G = nx.Graph()
for node in node_names:
    G.add_node(node)

for i, row in df.iterrows():
    comment = row['comment']
    reply = row['reply']
    weight = row['normalized_column']
    G.add_edge(comment, reply, weight=weight)

# Custom weight function
def custom_weight(edge_weight):
    return edge_weight

# Compute the layout with the custom weight function
pos = nx.spring_layout(G, weight=lambda u, v, d: custom_weight(d['weight']), iterations=500, seed=42)

# Compute the layout with the custom layout function
# pos = nx.kamada_kawai_layout(G, weight='weight')

# create edge trace
edge_x = []
edge_y = []
edge_lengths = df['normalized_column'].tolist()
for edge, length in zip(G.edges(), edge_lengths):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

# edge_weights = df['normalized_column'].tolist()

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

# create node trace
node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

# Create a dictionary with node names as keys and hover texts as values
hover_texts = {}
for i, row in df.iterrows():
    reply = row['reply']
    hover_text = row['comment text (eng)']
    hover_texts[reply] = hover_text


node_sizes = df['normalized_length'].tolist()

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='emrld',
        reversescale=True,
        color=node_colors,
        size=node_sizes,  # Set the node sizes based on the separate column
        sizemode='diameter',  # Use 'diameter' to set node sizes directly
        sizeref=0.5,  # Adjust the node sizes using a scaling factor
        sizemin=1,  # Set the minimum node size
        colorbar=dict(
            thickness=15,
            title='Sentiment Scores',
            xanchor='left',
            titleside='right'
        ),
        line_width=1))

# define the line length to make it visible in the graph
def insert_line_breaks(text, max_width=30):
    text = str(text)
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += f" {word}"
        else:
            lines.append(current_line.strip())
            current_line = word

    lines.append(current_line.strip())
    return "<br>".join(lines)

# Assign the hover texts to node_trace.text based on the node names
node_trace.text = [f'{node}<br>{insert_line_breaks(hover_texts.get(node, ""))}' for node in node_names]

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title=f"<br>{folder_name}",
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Text-Network Diagram",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.update_layout(plot_bgcolor='white')

# # Save the figure as an HTML file
# folder_path = "/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/results/conception"
# file_name = f"{folder_path}/{folder_name}_Network_Diagram.html"
# pio.write_html(fig, file=file_name)

fig.show()
