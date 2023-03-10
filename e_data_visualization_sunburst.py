import pandas as pd
import plotly.express as px
import plotly.io as pio

### Import data from the excel file and delete the null rows
df = pd.read_excel('x_final_data.xlsx')

###create our lists with parent and child values
comment = [str(x) for x in df['comment'].values.tolist()]
print('parent: ', comment)

reply_int = [str(x) for x in df['reply'].values.tolist()]
reply = [str(x) for x in reply_int]
print('child: ' , reply)

label = [str(x) for x in df['comment text'].values.tolist()]
print('label: ' , label)

value = df['sentiment scores'].values.tolist()
print('value: ', value)

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
    color_continuous_scale=px.colors.sequential.Emrld,  ### if it is numeric data --> check https://plotly.com/python/builtin-colorscales/#using-builtin-continuous-color-scales
    range_color=[-1, 1],

    ### define text
    branchvalues="total",  ### or 'remainder'
    # hover_name="comment",
    # hover_data={'comment': False},
    title="41. Magistrale Wandsbek",
    template='ggplot2',  ### 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                         ### 'plotly_white', 'plotly_dark', 'presentation',
                         ### 'xgridoff', 'ygridoff', 'gridon', 'none'
    maxdepth= -1,
)

### locate figure on plot by distance (top, left, right, bottom)
fig.update_layout(margin=dict(t=50, l=0, r=0, b=0),
                  coloraxis_colorbar_x=0.8, #location of the legend
                  title=dict(y=0.9, font=dict(size=15))) # size of the plot title

### update the size and font of the colorbar legend
# fig.update_coloraxes(colorbar_len=0.5,
#                      colorbar_thickness=15,
#                      colorbar_tickfont_size=10)

### hide the colorbar legend
fig.update_coloraxes(showscale=False)

fig.show()

#save the plot as png or jped
pio.write_image(fig, '41. Magistrale Wandsbek.png', format='png', width=1500, height=1500)
