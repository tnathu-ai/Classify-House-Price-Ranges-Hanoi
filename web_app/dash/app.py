import os

import dash  # version 1.13.1
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Data Exploration: Analyze House Price in Hanoi"

css_directory = os.getcwd()
stylesheets = ['stylesheet.css']
static_css_route = '/static/'


@app.server.route('{}<stylesheet>'.format(static_css_route))
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                stylesheet
            )
        )


def display_graphs(n_clicks):
    """
    This function will create a new plot graph and add to the div

    param n_clicks: this is an integer value act as an id to identify between plot
    return: div that contain the graph and the radio buton, with dropdown mennu
    """

    # if the n_clicks is 0 then it must be bar chart
    if n_clicks == 0:
        plot = 'bar'
    # if the n_clicks is 1 then it must be scatter chart
    elif n_clicks == 1:
        plot = 'scatter'
    # create a child as a div
    new_child = html.Div(
        # style of the div
        style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        # its children is a graph
        children=[
            dcc.Graph(
                # set the id and the type which will help make this graph dynamic in later process
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                # create an empty figure
                figure={}
            ),
            # create a radio item for selection, its default value is plot variable
            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                # option including bar chart or scatter chart
                options=[{'label': 'Bar Chart', 'value': 'bar'},
                         {'label': 'Scatter Chart', 'value': 'scatter'}, ],
                value=plot, className="card"
            ),
            # creat a dropdown to select the attribute
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-ctg',
                    'index': n_clicks
                },
                # create a label with value of 'House type', 'Legal documents',
                # 'No floor', 'No bedroom', and 'Day of Week' the replace function is to remove '_' and repace by space
                options=[{'label': c.replace('_', ' '), 'value': c} for c in ['House_type', 'Legal_documents',
                                                                              'No_floor', 'No_bedroom', 'Day_Of_Week']],
                # default is 'House_type'
                value='House_type',
                clearable=False
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-num',
                    'index': n_clicks
                },
                clearable=False
            )
        ],
        className="wrapper",
    )
    return new_child

# read the data from cleaned_data.csv which is a clean file
df = pd.read_csv("cleaned_data.csv", sep=',')

# the app layout
app.layout = html.Div([
    html.Div(children=[
        html.Div(
            children=[
                # title
                html.P(children="🙀", className="header-emoji"),
                html.H1(
                    children="House Price in Hanoi Analytics 2020", className="header-title",
                ),
            ],
            className="header",
        )
    ]),
    # this is the part where it contains 2 plot
    html.Div(id='container', children=[
        # create plot 1
        display_graphs(0),
        # create plot 2
        display_graphs(1)
    ])
])


@app.callback(
    [Output({'type': 'dynamic-dpn-num', 'index': MATCH}, 'options'),
     Output({'type': 'dynamic-dpn-num', 'index': MATCH}, 'value')],
    Input({'type': 'dynamic-choice', 'index': MATCH}, 'value'))
def dropdown_options(radio_value):
    """
    This function will base on the radio value to allows the dropdown menu to have certain value

    param radio_value: a string either 'bar' or 'scatter'
    return: an option for the dropbar menu, and the default value
    """
    # if the radio value is bar then the value can be 'Price', 'Area', 'Length', and 'Width'
    if radio_value == 'bar':
        options = [{'label': x, 'value': x} for x in ['Price', 'Area', 'Length', 'Width']]
        # set the default value as 'Price'
        value = 'Price'
    # if the radio value is scatter then the value will be exclude the 'Price' compare to the bar option
    else:
        options = [{'label': x, 'value': x} for x in ['Area', 'Length', 'Width']]
        # set the default value as 'Area'
        value = 'Area'
    # return the list of option and the default value
    return options, value


@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-ctg', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-num', 'index': MATCH}, component_property='value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
)
def update_graph(ctg_value, num_value, chart_choice):
    """
    This function will update the plot base on the radio button and the selection from two dropdown bar

    param ctg_value: this is the category value selection from the dropdown bar
    param num_value: this is the numerical value selection from the dropdown bar
    param chart_choice: this is the value from the radio button to choice the type of plot

    return: the update plot with the requirement
    """
    # if the chart choice is bar
    if chart_choice == 'bar':
        # group the selected category and selected the column with the selected numerical value
        # calculate the mean of numerical column with respect to the group of cateogircal value
        dff = df.groupby([ctg_value], as_index=False)[num_value].mean()
        # this is the y-axis string title
        prompt = {
            'Price': 'Average price in million VND per meter square',
            'Area': 'Average area in meter square',
            'Length': 'Average length in meter',
            'Width': 'Average width in meter'
        }
        # create a bar figure with the x-axis of categorical value, and y-axis as the numerical value
        fig = px.bar(dff, x=ctg_value, y=num_value, color_discrete_sequence=px.colors.sequential.Magenta,
                     labels={
                         # change the title of x-axis by replacing '_' with space
                         ctg_value: ctg_value.replace('_', ' '),
                         # change the title of y-axis by replacing it with the cooresponding value in the prompt
                         num_value: prompt[num_value]
                         # set the title name by combining the categorical value with numerical value
                     }, title=ctg_value.replace('_', ' ') + ' vs the average ' + num_value.lower() + ' bar plot')
        return fig
    # if the chart choice is scatter
    elif chart_choice == 'scatter':
        # this is the x-axis string title
        prompt = {
            'Area': 'Area in meter square',
            'Length': 'Length in meter',
            'Width': 'Width in meter'
        }
        # create a scatter figure with the x-axis as the numerical value, y axis as the Price,
        # and the category for the dots is the categorical value
        fig = px.scatter(df, x=num_value, y='Price', color=ctg_value,
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         labels={
                             # change the legend name by replacing '_' with space
                             ctg_value: ctg_value.replace('_', ' '),
                             # change the title of x-axis with the cooresponding value in the prompt
                             num_value: prompt[num_value],
                             # set the title of y-axis as given
                             'Price': 'Price (million VND per meter square)',
                             # set the title name by combing the categorical value with numerical value
                         }, title=num_value + ' vs the price with respect to ' + ctg_value.replace('_', ' '))
        return fig


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=True)
