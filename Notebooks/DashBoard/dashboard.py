# Import required libraries
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(
        id='id',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select Launch Site",
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=int(min_payload),
        max=int(max_payload),
        step=1000,
        marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1, 1000)},
        value=[int(min_payload), int(max_payload)],
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='id', component_property='value')
)
def get_pie_chart(selected_site):
    print(f"Pie chart callback triggered with site: {selected_site}")  # Debugging line
    filtered_df = spacex_df
    if selected_site == 'ALL':
        success_counts = filtered_df['class'].value_counts()
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        success_counts = filtered_df['class'].value_counts()
        
    fig = px.pie(
        values=success_counts,
        names=success_counts.index,
        title=f'Success vs Failure for {selected_site}' if selected_site != 'ALL' else 'Overall Success vs Failure'
    )
    print(fig)  # Debugging line to see if the figure is created
    return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='id', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    print(f"Scatter chart callback triggered with site: {selected_site} and payload range: {payload_range}")  # Debugging line
    filtered_df = spacex_df
    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= payload_range[0]) & 
        (filtered_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        
    print(filtered_df)  # Debugging line to check filtered DataFrame
    
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Payload Mass (kg)',
        title='Payload vs. Launch Success'
    )
    print(fig)  # Debugging line to see if the figure is created
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
