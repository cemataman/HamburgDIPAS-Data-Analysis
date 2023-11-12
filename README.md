# DIPAS Hamburg Data Analysis

The DIPAS dataset comprises textual data collected from a digital participation platform in Hamburg, Germany. 
This platform serves as a venue for residents to engage in ongoing urban design and planning projects. 
Although the dataset is confidential, the platform is publicly accessible, and all contributions are visible on the website.

## Data Description

The dataset encompasses a variety of projects, each of which includes data regarding the geolocations and timestamps of comments and replies. 
Given that the duration of projects and the length of discussions vary, several normalization steps are implemented during the preprocessing phase. 
The DIPAS dataset is multifaceted: it incorporates multiple projects, each containing an array of discussion topics. 
These topics, in turn, feature numerous comments and replies. 
Consequently, a hierarchical analysis of the dataset is imperative.

## Citation
Please include the following citation if you are interested in using the introduced methods:

Ataman, Cem, Bige Tuncer, and Simon Perrault. 2022. ”Asynchronous Digital Participation in Urban Design Processes: Qualitative Data Exploration and Analysis with Natural Language Processing”. In *POST-CARBON - Proceedings of the 27th Conference on Computer-Aided Architectural Design Research in Asia (CAADRIA),* 383–92, Sydney, Australia.

## How to Use the Code

It is advisable to adhere to the sequence of the following five steps when executing the code:

1. Execute the **data_cleaning.py** file to preprocess the data.
2. Subsequently, run **data_extraction.py** to hierarchically structure the data for use in visualization.
3. Execute **data_translation.py** to translate text from German to English.
4. Run **sentiment_analysis.py** to perform sentiment analysis on the preprocessed data.
5. Execute **BerTopic_Model.py** to construct a topic model based on the selected dataset.

Completing these five steps will yield structured data frames and results that can be utilized in subsequent analyses. 
After the data frames and the topic model have been created, the visualization scripts may be employed according to the requirements of the analysis. 
Please make sure to replace the file path with that of your own dataset.

### Folders and Scripts

- **Scripts**: A folder containing all the relevant scripts.
    - *data_cleaning.py*: Responsible for preprocessing textual data.
    - *data_extraction.py*: Serves to structure the data frame.
    - *data_translation.py*: Translates data from German to English (Note: D7 and D8 are distinct data structures, yet the translation script is applicable to both).
    - *sentiment_analysis.py*: Computes the sentiment scores for each argument.
    - *BerTopic_Model.py*: Formulates a BERTopic model based on the final dataset.
    - **Visualizations**
        - *data_visualization_topic_model.py*: Offers four methods for visualization, including a similarity matrix, hierarchical structures, an intertopic distance map, and topics alongside dominant words.
        - *data_visualization_sunburst.py*: Utilizes sunburst diagrams to represent the hierarchical structure of the arguments, complete with sentiment scores.
        - *data_visualization_text_network_2D.py*: Provides 2D text-network diagrams to visualize temporal and length-related aspects of the discussions.
        - *data_visualization_text_network_3D.py*: Features 3D text-network diagrams to serve the same purpose in a more comprehensive manner.
    - **data_visualization_interactive_map**
        - *map.js*: Creates an interactive map with Leaflet.js, displaying custom-colored markers based on sentiment scores from CSV file data.
        - *index.html*: Creates a webpage with an interactive map, integrating external Leaflet.js and PapaParse libraries, and includes a CSV file upload input and a div for the map display.
    - **for multiple files**
        - *data_translation.py*: Translates data from German to English (Note: D7 and D8 are distinct data structures, yet the translation script is applicable to both).
        - *sentiment_analysis.py*: Computes the sentiment scores for each argument.
        - *data_visualization_sunburst.py*: Utilizes sunburst diagrams to represent the hierarchical structure of the arguments, complete with sentiment scores.
