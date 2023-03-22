import os
import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.io as pio

# specify the directory path where you want to search for xlsx files
directory_path = "/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/data/Drupal 8 (2020-21)"

# specify the folder path where you want to save the output files
result_folder = "/Users/cem_ataman/PycharmProjects/HamburgDIPAS-Data-Analysis/results/conception"

# loop through all folders in the directory
for folder_name in os.listdir(directory_path):
    folder_path = os.path.join(directory_path, folder_name)
    # check if the folder contains the target xlsx file
    file_path = os.path.join(folder_path, "conceptioncomments_structured.xlsx")
    engine = 'openpyxl'

    if os.path.isfile(file_path):
        # read the xlsx file into a DataFrame
        df = pd.read_excel(file_path, engine=engine)

        ### Sort the dataframe based on the sentiment scores in ascending order
        df = df.sort_values(by='sentiment scores')

        ###create our lists with parent and child values
        comment = [str(x) for x in df['comment'].values.tolist()]
        # print('parent: ', comment)

        reply_int = [str(x) for x in df['reply'].values.tolist()]
        reply = [str(x) for x in reply_int]
        # print('child: ' , reply)

        label = [str(x) for x in df['comment text (eng)'].values.tolist()]
        # print('label: ' , label)

        value = df['sentiment scores'].values.tolist()
        # print('value: ', value)

        ###create our data as dictionary
        data = dict(
            character=reply,
            parent=comment,
            labels=label,
            value=value
        )

        ### Define the Sunburst features
        fig = px.sunburst(
            data,
            names='character',
            parents='parent',
            hover_name="labels",
            # hover_data={'comment': False},

            ### define color
            color="value",
            # color_discrete_sequence=px.colors.qualitative.Pastel, ### if it is textual data
            color_continuous_scale=px.colors.sequential.Emrld,
            ### if it is numeric data --> check https://plotly.com/python/builtin-colorscales/#using-builtin-continuous-color-scales
            range_color=[-1, 1],

            ### define text
            branchvalues="total",  ### or 'remainder'
            # hover_name="comment",
            # hover_data={'comment': False},
            title= f"{folder_name}",
            template='ggplot2',  ### 'ggplot2', 'seaborn', 'simple_white', 'plotly',
            ### 'plotly_white', 'plotly_dark', 'presentation',
            ### 'xgridoff', 'ygridoff', 'gridon', 'none'
            maxdepth=-1,
        )

        ### locate figure on plot by distance (top, left, right, bottom)
        fig.update_layout(margin=dict(t=50, l=0, r=0, b=0),
                          coloraxis_colorbar_x=0.8,  # location of the legend
                          title=dict(y=0.9, font=dict(size=15)))  # size of the plot title

        ### update the size and font of the colorbar legend
        # fig.update_coloraxes(colorbar_len=0.5,
        #                      colorbar_thickness=15,
        #                      colorbar_tickfont_size=10)

        fig.update_coloraxes(
            colorbar_len=0.5,
            colorbar=dict(
                title="Sentiment Score",
                titleside='right',
                thickness=20,
                tickmode="auto",
                ticks="inside",
                ticklen=5,
                tickfont=dict(size=10),
                titlefont=dict(size=12)
            )
        )

        ### hide the colorbar legend
        fig.update_coloraxes(showscale=True)

        # save the plot as PNG
        result_path = os.path.join(result_folder, f"{folder_name}_conception.png")
        pio.write_image(fig, result_path, format='png', width=2000, height=1200)

        # save the plot as HTML
        html_result_path = os.path.join(result_folder, f"{folder_name}_conception.html")
        pio.write_html(fig, html_result_path)
