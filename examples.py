""" Create a simple dashboard with plotly Dash. """

# Run this app with 'python run.py' and open the browser at 
# http://localhost:8050/

from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import json
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

my_input = dcc.Input(value='initial value', type='text')
my_output = html.Div()

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# DASH LAYOUT
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

df3 = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')


fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Interactive Visualizations

df4 = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "customdata": [1,2,3,4],
    "fruit": ["apple", "apple", "orange", "orange"]
})

fig2 = px.scatter(df4, x="x", y="y", color="fruit", custom_data=["customdata"])

fig2.update_layout(clickmode='event+select')

fig2.update_traces(marker_size=20)


# Table
df5 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


# Update Graphs on Hover
df6 = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')


# Generic Crossfilter Recipe
# make a sample data frame with 6 columns
np.random.seed(0)  # no-display
df7 = pd.DataFrame({"Col " + str(i+1): np.random.rand(30) for i in range(6)})

def get_figure(df, x_col, y_col, selectedpoints, selectedpoints_local):

    if selectedpoints_local and selectedpoints_local['range']:
        ranges = selectedpoints_local['range']
        selection_bounds = {'x0': ranges['x'][0], 'x1': ranges['x'][1],
                            'y0': ranges['y'][0], 'y1': ranges['y'][1]}
    else:
        selection_bounds = {'x0': np.min(df[x_col]), 'x1': np.max(df[x_col]),
                            'y0': np.min(df[y_col]), 'y1': np.max(df[y_col])}

    # set which points are selected with the `selectedpoints` property
    # and style those points with the `selected` and `unselected`
    # attribute. see
    # https://medium.com/@plotlygraphs/notes-from-the-latest-plotly-js-release-b035a5b43e21
    # for an explanation
    fig = px.scatter(df, x=df[x_col], y=df[y_col], text=df.index)

    fig.update_traces(selectedpoints=selectedpoints,
                      customdata=df.index,
                      mode='markers+text', marker={ 'color': 'rgba(0, 116, 217, 0.7)', 'size': 20 }, unselected={'marker': { 'opacity': 0.3 }, 'textfont': { 'color': 'rgba(0, 0, 0, 0)' } })

    fig.update_layout(margin={'l': 20, 'r': 0, 'b': 15, 't': 5}, dragmode='select', hovermode=False)

    fig.add_shape(dict({'type': 'rect',
                        'line': { 'width': 1, 'dash': 'dot', 'color': 'darkgrey' } },
                       **selection_bounds))
    return fig


markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app.layout = html.Div(
    children=[
        html.Div(
            style={
                'backgroundColor': colors['background']
            },
            children=[
                html.H1(
                    children='LAYOUT'
                ),
                html.H1(
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    },
                    children='Hello Dash'
                ),

                html.Div(
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    },
                    children='''
                    Dash: A web application framework for your data.
                    '''
                ),

                dcc.Graph(
                    id='example-graph',
                    figure=fig
                ),
            ]
        ),
        html.Div(
            children = [ 
                html.Br(),
                html.H1(
                    children='Reusable Components'
                ),
                html.H4(children='US Agriculture Exports (2011)'),
                generate_table(df5),
            ]
        ),
        html.Div(
            children = [ 
                html.Br(),
                html.H1(
                    children='Markdown'
                ),
                html.H4(children='Markdown'),
                html.Div(children=markdown_text),
            ]
        ),
        html.Div(
            style={
                'display': 'flex',
                'flex-direction': 'row'
            },
            children = [
                html.Br(),
                html.H1(
                    children='Core Components'
                ),
                html.Div(
                    style={
                        'padding': 10,
                        'flex': 1
                    },
                    children=[
                        html.Label('Dropdown'),
                        dcc.Dropdown(
                            ['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

                        html.Br(),
                        html.Label('Multi-Select Dropdown'),
                        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                                    ['Montréal', 'San Francisco'],
                                    multi=True),

                        html.Br(),
                        html.Label('Radio Items'),
                        dcc.RadioItems(
                            ['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
                    ]
                ),
                html.Div(
                    style={
                        'padding': 10,
                        'flex': 1
                    },
                    children=[
                        html.Label('Checkboxes'),
                        dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                                    ['Montréal', 'San Francisco']
                        ),

                        html.Br(),
                        html.Label('Text Input'),
                        dcc.Input(value='MTL', type='text'),

                        html.Br(),
                        html.Label('Slider'),
                        dcc.Slider(
                            min=0,
                            max=9,
                            marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
                            value=5,
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            children = [
                html.Br(),
                html.H1(
                    children='Simple Interactive Dash App'
                ),
                html.H6(
                    "Change the value in the text box to see callbacks in action!"
                ),
                html.Div(
                    [
                        "Input: ",
                        dcc.Input(
                            id='my-input',
                            value='initial value',
                            type='text'
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    id='my-output'
                ),
            ]
        ),
        html.Div(
            children = [
                html.Br(),
                html.H1(
                    children='Dash App Layout With Figure and Slider'
                ),
                dcc.Graph(id='graph-with-slider'),
                dcc.Slider(
                    df2['year'].min(),
                    df2['year'].max(),
                    step=None,
                    value=df2['year'].min(),
                    marks={
                        str(year): str(year) for year in df2['year'].unique()
                    },
                    id='year-slider'
                )
            ]
        ),
        html.Div(
            children = [
                html.Br(),
                html.H1(
                    children='Dash App With Multiple Inputs'
                ),
                html.Div(
                    children = [
                        html.Div(
                            style={
                                'width': '48%',
                                'display': 'inline-block'
                            },
                            children= [
                                dcc.Dropdown(
                                    df3['Indicator Name'].unique(),
                                    'Fertility rate, total (births per woman)',
                                    id='xaxis-column'
                                ),
                                dcc.RadioItems(
                                    ['Linear', 'Log'],
                                    'Linear',
                                    id='xaxis-type',
                                    inline=True
                                )
                            ],
                        ),
                        html.Div(
                            style={
                                'width': '48%',
                                'float': 'right',
                                'display': 'inline-block'
                            },
                            children = [
                                dcc.Dropdown(
                                    df3['Indicator Name'].unique(),
                                    'Life expectancy at birth, total (years)',
                                    id='yaxis-column'
                                ),
                                dcc.RadioItems(
                                    ['Linear', 'Log'],
                                    'Linear',
                                    id='yaxis-type',
                                    inline=True
                                )
                            ]
                        )
                    ],
                ),
                dcc.Graph(id='indicator-graphic'),
                dcc.Slider(
                    df3['Year'].min(),
                    df3['Year'].max(),
                    step=None,
                    id='year--slider',
                    value=df3['Year'].max(),
                    marks={
                        str(year): str(year) for year in df3['Year'].unique()
                    },
                )
            ]
        ),
        html.Div(
            children =[
                html.Br(),
                html.H1(
                    children='Dash App With Multiple Outputs'
                ),
                dcc.Input(
                    id='num-multi',
                    type='number',
                    value=5
                ),
                html.Table(
                    [
                        html.Tr(
                            [
                                html.Td(
                                    ['x', html.Sup(2)]
                                ),
                                html.Td(
                                    id='square'
                                )
                            ]
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    [
                                        'x',
                                        html.Sup(3)
                                    ]
                                ),
                                html.Td(
                                    id='cube'
                                )
                            ]
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    [
                                        2,
                                        html.Sup('x')
                                    ]
                                ),
                                html.Td(
                                    id='twos'
                                )
                            ]
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    [
                                        3,
                                        html.Sup('x')
                                    ]
                                ),
                                html.Td(
                                    id='threes'
                                )
                            ]
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    [
                                        'x',
                                        html.Sup('x')
                                    ]
                                ),
                                html.Td(
                                    id='x^x'
                                )
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            children = [
                html.Br(),
                html.H1(
                    children='Dash App With Chained Callbacks'
                ),
                dcc.RadioItems(
                    list(all_options.keys()),
                    'America',
                    id='countries-radio',
                ),

                html.Hr(),

                dcc.RadioItems(id='cities-radio'),

                html.Hr(),

                html.Div(id='display-selected-values')
            ]
        ),
        html.Div(
            children=[
                html.Br(),
                html.H1(
                    children='Dash App With State'
                ),
                dcc.Input(
                    id="input-1",
                    type="text",
                    value="Montréal"
                ),
                dcc.Input(
                    id="input-2",
                    type="text",
                    value="Canada"
                ),
                html.Div(
                    id="number-output"
                ),
            ]
        ),
        html.Div(
            children=[
                html.Br(),
                html.H1(
                    children='Dash App With State 2'
                ),
                dcc.Input(
                    id='input-1-state',
                    type='text',
                    value='Montréal'
                ),
                dcc.Input(
                    id='input-2-state',
                    type='text',
                    value='Canada'
                ),
                html.Button(
                    id='submit-button-state',
                    n_clicks=0,
                    children='Submit'
                ),
                html.Div(
                    id='output-state'
                )
            ]
        ),
        html.Div(
            children=[
                html.Br(),
                html.H1(
                    children='Passing Components Into Callbacks Instead of IDs'
                ),
                html.H6(
                    "Change the value in the text box to see callbacks in action!"
                ),
                html.Div(
                    [
                        "Input: ",
                        my_input
                    ]
                ),
                html.Br(),
                my_output
            ]
        ),
        html.Div(
            children=[
                html.Br(),
                html.H1(
                    children='Interactive Visualizations'
                ),
                dcc.Graph(
                    id='basic-interactions',
                    figure=fig2
                ),

                html.Div(
                    className='row',
                    children=[
                        html.Div(
                            className='three columns',
                            children=[
                                dcc.Markdown("""
                                    **Hover Data**

                                    Mouse over values in the graph.
                                """),
                                html.Pre(
                                    id='hover-data',
                                    style=styles['pre']
                                )
                            ]
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                dcc.Markdown("""
                                    **Click Data**

                                    Click on points in the graph.
                                """),
                                html.Pre(
                                    id='click-data',
                                    style=styles['pre']
                                ),
                            ]
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                dcc.Markdown("""
                                    **Selection Data**

                                    Choose the lasso or rectangle tool in the graph's menu
                                    bar and then select points in the graph.

                                    Note that if `layout.clickmode = 'event+select'`, selection data also
                                    accumulates (or un-accumulates) selected data if you hold down the shift
                                    button while clicking.
                                """),
                                html.Pre(
                                    id='selected-data',
                                    style=styles['pre']
                                ),
                            ]
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                dcc.Markdown("""
                                    **Zoom and Relayout Data**

                                    Click and drag on the graph to zoom or click on the zoom
                                    buttons in the graph's menu bar.
                                    Clicking on legend items will also fire
                                    this event.
                                """),
                                html.Pre(
                                    id='relayout-data',
                                    style=styles['pre']
                                ),
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            children=[
                html.Br(),
                html.H1(
                    children='Update Graphs on Hover'
                ),
                html.Div(
                    style={
                        'padding': '10px 5px'
                    },
                    children=[
                        html.Div(
                            style={'width': '49%', 'display': 'inline-block'},
                            children=[
                                dcc.Dropdown(
                                    df6['Indicator Name'].unique(),
                                    'Fertility rate, total (births per woman)',
                                    id='crossfilter-xaxis-column',
                                ),
                                dcc.RadioItems(
                                    ['Linear', 'Log'],
                                    'Linear',
                                    id='crossfilter-xaxis-type',
                                    labelStyle={
                                        'display': 'inline-block',
                                        'marginTop': '5px'
                                    }
                                )
                            ],
                        ),
                        html.Div(
                            style={
                                'width': '49%',
                                'float': 'right',
                                'display': 'inline-block'
                            },
                            children=[
                                dcc.Dropdown(
                                    df6['Indicator Name'].unique(),
                                    'Life expectancy at birth, total (years)',
                                    id='crossfilter-yaxis-column'
                                ),
                                dcc.RadioItems(
                                    ['Linear', 'Log'],
                                    'Linear',
                                    id='crossfilter-yaxis-type',
                                    labelStyle={
                                        'display': 'inline-block',
                                        'marginTop': '5px'
                                    }
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={
                        'width': '49%',
                        'display': 'inline-block',
                        'padding': '0 20'
                    },
                    children=[
                        dcc.Graph(
                            id='crossfilter-indicator-scatter',
                            hoverData={
                                'points': [
                                    {
                                        'customdata': 'Japan'
                                    }
                                ]
                            }
                        )
                    ]
                ),
                html.Div(
                    style={'display': 'inline-block', 'width': '49%'},
                    children=[
                        dcc.Graph(id='x-time-series'),
                        dcc.Graph(id='y-time-series'),
                    ]
                ),
                html.Div(
                    style={'width': '49%', 'padding': '0px 20px 20px 20px'},
                    children=[
                        dcc.Slider(
                            df6['Year'].min(),
                            df6['Year'].max(),
                            step=None,
                            id='crossfilter-year--slider',
                            value=df6['Year'].max(),
                            marks={
                                str(year): str(year) for year in df6['Year'].unique()
                            }
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='four columns',
                    children=[
                        dcc.Graph(
                            id='g1',
                            config={'displayModeBar': False}
                        )
                    ]
                ),
                html.Div(
                    className='four columns',
                    children=[
                        dcc.Graph(
                            id='g2',
                            config={
                                'displayModeBar': False
                            }
                        )
                    ],
                ),
                html.Div(
                    className='four columns',
                    children=[
                        dcc.Graph(
                            id='g3',
                            config={
                                'displayModeBar': False
                            }
                        )
                    ],
                )
            ]
        )
    ]
)


# Simple Interactive Dash App
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'


# Dash App Layout With Figure and Slider
@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df2[df2['year'] == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)
    return fig


# Dash App With Multiple Inputs
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df3[df3['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig


# Dash App With Multiple Outputs
@app.callback(
    Output('square', 'children'),
    Output('cube', 'children'),
    Output('twos', 'children'),
    Output('threes', 'children'),
    Output('x^x', 'children'),
    Input('num-multi', 'value'))
def callback_a(x):
    return x**2, x**3, 2**x, 3**x, x**x


# Dash App With Chained Callbacks
@app.callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
    Output('cities-radio', 'value'),
    Input('cities-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value'))
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )


# Dash App With State
@app.callback(
    Output("number-output", "children"),
    Input("input-1", "value"),
    Input("input-2", "value"),
)
def update_output(input1, input2):
    return u'Input 1 is "{}" and Input 2 is "{}"'.format(input1, input2)


# Dash App With State 2
@app.callback(Output('output-state', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
def update_output(n_clicks, input1, input2):
    return u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(n_clicks, input1, input2)


# Passing Components Into Callbacks Instead of IDs
@app.callback(
    Output(my_output, component_property='children'),
    Input(my_input, component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'


# Interactive Visualizations
@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)

@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


# Update Graphs on Hover
@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('crossfilter-year--slider', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df6[df6['Year'] == year_value]

    fig6 = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
            )

    fig6.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig6.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig6.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig6.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig6

def create_time_series(dff, axis_type, title):

    fig6 = px.scatter(dff, x='Year', y='Value')

    fig6.update_traces(mode='lines+markers')

    fig6.update_xaxes(showgrid=False)

    fig6.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig6.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig6.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig6

@app.callback(
    Output('x-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'))
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df6[df6['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

@app.callback(
    Output('y-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-yaxis-type', 'value'))
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df6[df6['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

# Generic Crossfilter Recipe
# this callback defines 3 figures
# as a function of the intersection of their 3 selections
@app.callback(
    Output('g1', 'figure'),
    Output('g2', 'figure'),
    Output('g3', 'figure'),
    Input('g1', 'selectedData'),
    Input('g2', 'selectedData'),
    Input('g3', 'selectedData')
)
def callback(selection1, selection2, selection3):
    selectedpoints = df7.index
    for selected_data in [selection1, selection2, selection3]:
        if selected_data and selected_data['points']:
            selectedpoints = np.intersect1d(selectedpoints,
                [p['customdata'] for p in selected_data['points']])

    return [get_figure(df7, "Col 1", "Col 2", selectedpoints, selection1),
            get_figure(df7, "Col 3", "Col 4", selectedpoints, selection2),
            get_figure(df7, "Col 5", "Col 6", selectedpoints, selection3)]

if __name__ == '__main__':
    app.run_server(debug=True)
