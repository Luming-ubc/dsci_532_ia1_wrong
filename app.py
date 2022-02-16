# plot altair
from dash import Input, Output
from dash import Dash, html, dcc
import altair as alt
from vega_datasets import data

cars = data.cars()

# slider plot


def plot_altair(xmax, df=cars.copy()):
    chart = alt.Chart(df[df['Horsepower'] < xmax]).mark_point().encode(
        x='Horsepower',
        y='Weight_in_lbs')
    return chart.to_html()


# create dashboard

app = Dash(__name__, external_stylesheets=[
           'https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    # Dashboard Title
    html.Div("Welcome to Luming's Pilot Dashboard",
             style={'color': 'blue', 'fontSize': 44, 'background-color': 'lightblue'}),

    # Slider
    'Hi, I am a simple slider at value 2',
    dcc.Slider(min=0, max=5, value=2, marks={0: '0', 5: '5'}),
    'Hi, I am a slider ranges from 1 to 3',
    dcc.RangeSlider(min=0, max=5, value=[1, 3], marks={0: '0', 5: '5'}),

    # Color text box
    html.P('Hi, I am orange', id='my-para',
           style={'background-color': 'orange'}),

    # break
    'Hi, I am a break',
    html.Br(),
    html.Br(),

    # Dropdown
    'Hi, I am single dropdown',
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'San Francisco', 'value': 'SF'}],
        placeholder='Select a city...',
        value='SF'),

    html.Br(),
    html.Br(),

    'Hi, I am multiple dropdown',
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'San Francisco', 'value': 'SF'}],
        placeholder='Select one or more city...',
        value='SF', multi=True),

    html.Br(),
    html.Br(),

    # link widget ID with call back functions
    'Hi, I repeat what you type',
    html.Br(),
    dcc.Input(id='widget-1'),
    html.Br(),
    # 'Textarea is not desirable',
    # dcc.Textarea(id='widget-2'),
    html.Br(),
    html.Div(id='widget-2'),

    html.Br(),

    # add altair plot - slider
    'Hi, I select range of Horsepower for the plot below:',
    dcc.Slider(id='xslider', min=0, value=120, max=240),  # slider
    html.Iframe(id='scatter',
                srcDoc=plot_altair(xmax=240),
                style={'border-width': '0', 'width': '100%', 'height': '400px'}),  # fix size


    # add altair plot - dropdown
    'Hi, I select category for x axis in the plot below:',
    dcc.Dropdown(
        id='xcol-widget', value='Horsepower',
        options=[{'label': i, 'value': i} for i in cars.columns]),
    html.Iframe(
        id='scatter_drop',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    # srcDoc=plot_altair_drop(xcol='Horsepower')), # make it elegant



], style={'marginTop': 50})


# call back functions


@ app.callback(
    # Output('widget-2', 'value'),
    Output('widget-2', 'children'),
    Input('widget-1', 'value'))
def update_output(input_value):
    return input_value

# call back function - scatter plot - traditional


@ app.callback(
    Output('scatter', 'srcDoc'),
    Input('xslider', 'value'))
def update_output(xmax):
    return plot_altair(xmax)

# call back function

# drop down plot


@ app.callback(
    Output('scatter_drop', 'srcDoc'),
    Input('xcol-widget', 'value'))
def plot_altair_drop(xcol):
    chart = alt.Chart(cars).mark_point().encode(
        x=xcol,
        y='Displacement',
        tooltip='Horsepower').interactive()
    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
