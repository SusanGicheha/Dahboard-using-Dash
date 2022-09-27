
import dash
from dash import html
from dash import dcc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from dash.dependencies import Output, Input

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # initialising dash app
app.title = "Dash !" #name on the tabs


# df = px.data.stocks()  # reading stock price dataset
county = pd.read_csv("county data.csv")
country = pd.read_csv("Covid Kenya.csv")
county_vaccinated = pd.read_csv("county_vaccinated.csv")

# convert date column to proper date format
country['date'] = pd.to_datetime(country['date'])
country['month'] = pd.DatetimeIndex(country['date']).month
country['year'] = pd.DatetimeIndex(country['date']).year
#country=country.set_index('date')
country['total_cases']=pd.to_numeric(country['total_cases'])
country['new_deaths']=pd.to_numeric(country['new_deaths'])
country['total_deaths']=pd.to_numeric(country['total_deaths'])
country['total_deaths'] = country['total_deaths'].fillna(0)
country['total_tests']=country['total_tests'].fillna(0)
country['cumulative recovered'] = country['cumulative recovered'].fillna(0)
country['percent']=pd.to_numeric(country['positive_rate']*100)
country.dropna(subset = ["percent"], inplace=True)



# function which will render bar graph for run scored by player
app.layout = html.Div( children=[
        html.Div(
            children=[
                html.H1(
                    children="Covid-19 Analysis", className="header-title"
                ),
                html.H4('Last Updated On ' +str(country['date'].iloc[-1].strftime("%B %d, %Y")), style={'color':'red', 'textAlign': 'center'}),
            ],
            className="header"
        ),
    #grids
 html.Div([

     ##totalcases
html.Div([
        html.H4(children='Total Cases ', style={'textAlign': 'center', 'color': 'red', 'fontSize': 20}
                 ),
         html.P(f"{country['total_cases'].iloc[-1]:,.0f}",
                style={'textAlign': 'center', 'color': 'red', 'fontSize': 40}
                ),
        html.P('new: '+f"{country['total_cases'].iloc[-1] - country['total_cases'].iloc[-2]:,.0f}"
               + ' ('+ str(round(((country['total_cases'].iloc[-1] - country['total_cases'].iloc[-2]) /
                     country['total_cases'].iloc[-1])*100,2)) + '%)',
                           style={
                               'textAlign':'center',
                               'color':'red',
                               'fontSize':15,
                               'margin-top': '-18px'

                           })],
),
    #total deaths
html.Div([
        html.H4(children='Total Deaths ', style={'textAlign': 'center', 'color': 'red', 'fontSize': 20}
                 ),
         html.P(f"{country['total_deaths'].iloc[-1]:,.0f}",
                style={'textAlign': 'center', 'color': 'red', 'fontSize': 40}
                ),
        html.P('new: '+f"{country['total_deaths'].iloc[-1] - country['total_deaths'].iloc[-2]:,.0f}"
               + ' ('+ str(round(((country['total_deaths'].iloc[-1] - country['total_deaths'].iloc[-2]) /
                     country['total_deaths'].iloc[-1])*100,2)) + '%)',
                           style={
                               'textAlign':'center',
                               'color':'red',
                               'fontSize':15,
                               'margin-top': '-18px'

                           })],
),
     #total recovered
html.Div([
        html.H4(children='Total Recoveries ', style={'textAlign': 'center', 'color': 'red', 'fontSize': 20}
                 ),
         html.P(f"{country['cumulative recovered'].iloc[-1]:,.0f}",
                style={'textAlign': 'center', 'color': 'red', 'fontSize': 40}
                ),
        html.P('new: '+f"{country['cumulative recovered'].iloc[-1] - country['cumulative recovered'].iloc[-2]:,.0f}"
               + ' ('+ str(round(((country['cumulative recovered'].iloc[-1] - country['cumulative recovered'].iloc[-2]) /
                     country['total_deaths'].iloc[-1])*100,2)) + '%)',
                           style={
                               'textAlign':'center',
                               'color':'red',
                               'fontSize':15,
                               'margin-top': '-18px'

                           })],
),

], className="grid-container"),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="county-cases",
                        config={"displayModeBar":False},

                        figure={
                            "data" : [
                                {
                                    "x" : county["County"],
                                    "y" : county["Cumulative Cases"],
                                    "type" : "bar",
                                    "title": "Cases per county"
                                },
                            ],
                            "layout" : {

                                "xaxis": {"fixedrange" : True, "title":"Counties"},
                                "yaxis": { "fixedrange": True, "title":"No. of cases", },
                                "colorway": ["#d62728"],
                                "title" : "Total Number of Cases Per County",

                            },
                        },
                    ),
                    className="card",
                ),
            ],
        ),
])



if __name__ == '__main__':
     app.run_server(debug=True, port=8080)
