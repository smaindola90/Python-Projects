''' In this project, I created a dashboard for Spacex launch cites data.
The dashboard is created using plotly dash.'''

# Importing required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Reading the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Creating a dash application
app = dash.Dash(__name__)

# Creating an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Adding a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                ],
                                             value='ALL',
                                             placeholder='Select a Launch Site',
                                             searchable=True
                                             ),
                                html.Br(),

                                # Adding a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, showing the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # Adding a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0:'0', 1000:'1000', 2000:'2000', 3000:'3000', 4000:'4000', 5000:'5000', 6000:'6000', 7000:'7000', 8000:'8000', 9000:'9000', 10000:'10000'},
                                                value=[min_payload, max_payload]),

                                # Adding a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Adding a callback function for 'site-dropdown' as input, 'success-pie-chart' as output
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[['Launch Site', 'class']].groupby(['Launch Site'], as_index=False).sum()
        filtered_df.rename(columns={'class':'Successes'}, inplace=True)
        fig = px.pie(filtered_df, values='Successes', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site].groupby(['class'], as_index=False).count()
        col = ['Failure', 'Success']
        filtered_df['Outcome']=col
        filtered_df.rename(columns={'Launch Site':'Count'}, inplace=True)
        
        fig = px.pie(filtered_df, values='Count', names='Outcome', title=f"Total Success Launches for site {entered_site}", color='Outcome', color_discrete_map={'Failure':'tomato', 'Success':'royalblue'})
        return fig

# Adding a callback function for 'site-dropdown' and 'payload-slider' as inputs, 'success-payload-scatter-chart' as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])

def get_scatter_chart(entered_site, slider_value):
    low, high = slider_value
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(low, high, inclusive=True)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color = 'Booster Version Category', title=f"Correlation between Payload and Success for {entered_site} Launch Site")
        return fig

# Running the app
if __name__ == '__main__':
    app.run_server()
