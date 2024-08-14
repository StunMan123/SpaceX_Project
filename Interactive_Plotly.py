"""
terminal:
python3.11 -m pip install pandas dash
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
python3.11 spacex_dash_app.py
"""

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


#html.Br() => line break
#html.Div() => division, group together other html components
#html.H1() => heading level 1


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

#options for dropdown
options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options = options,
                                    value='ALL',
                                    searchable = True,
                                    placeholder='Select a Launch Site here'),

                                html.Br(), 

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    #step is the interval of changes when you pull the range slider
                                    min=0, max=10000, step=1000,
                                    #marks is the label show in rangeslider
                                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                    value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site, ):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Success vs. Failed counts for ALL')
        return fig
    # return the outcomes piechart for a selected site
    else :
        site_data = filtered_df[filtered_df['Launch Site'] == entered_site]
        success_counts = site_data['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        fig = px.pie(success_counts, 
        values='count', 
        names='class', 
        title=f'Success vs. Failed counts for {entered_site}')
        return fig        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
                         color="Booster Version Category", 
                         title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        site_data = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_data, x="Payload Mass (kg)", y="class", 
                         color="Booster Version Category", 
                         title=f'Correlation between Payload and Success for {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


"""
references

dcc.Dropdown() => https://dash.plotly.com/dash-core-components/dropdown
dcc.RangeSlider() => https://dash.plotly.com/dash-core-components/rangeslider
pie chart => https://plotly.com/python/pie-charts/
scatter chart => https://plotly.com/python/line-and-scatter/

"""