
import dash
import flask
from dash import html
from dash import dcc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])  # initialising dash app
server = app.server
app.title = "Covid 19 Kenya Dashboard"
# name on the tabs


# df = px.data.stocks()  # reading stock price dataset
county = pd.read_csv("county data.csv")
country = pd.read_csv("Covid Kenya.csv")
county_vaccinated = pd.read_csv("county_vaccinated.csv")

# convert date column to proper date format
country['date'] = pd.to_datetime(country['date'])
country['month'] = pd.DatetimeIndex(country['date']).month
country['year'] = pd.DatetimeIndex(country['date']).year
value_confirmed = round(country['total_deaths'].iloc[-1] / country['total_cases'].iloc[-1] * 100)
value_remain = round(100 - country['total_deaths'].iloc[-1] / country['total_cases'].iloc[-1] * 100)
value_confirmed2 = round(country['cumulative recovered'].iloc[-1] / country['total_cases'].iloc[-1] * 100)
value_remain2 = round(100 - country['cumulative recovered'].iloc[-1] / country['total_cases'].iloc[-1] * 100)

# country=country.set_index('date')




# function which will render bar graph for run scored by player
app.layout = html.Div(children=[
        html.Div(
            children=[
              #  html.Img(src=('assets/262cfac.png'), style={'height':'60px', 'width':'60px'}),
                html.H5(
                    children="COVID-19 IN KENYA", className="header-title", style={'color':'black', 'textAlign': 'center','fontSize':20,"background-color":"#ffffff"}
                ),
            html.H6('Last Updated On ' +str(country['date'].iloc[-1].strftime("%B %d, %Y")), className='header-title',style={'color':'black', 'textAlign': 'center', 'margin-top':'10px'}),
            ], style={"border-bottom":"1px solid","border-radius": "3px", "background-color":"#ffffff", "border-color": "#c0c0c0"}

        ),
    #grids
    html.Div([
        html.Div([

            #grid for tallys
 html.Div([
     ##totalcases
html.Div([

        html.H5(children='Total Cases', style={'textAlign': 'center', 'color': 'black', 'fontSize': 20}
                 ),
         html.P(f"{country['total_cases'].iloc[-1]:,.0f}",
                style={'textAlign': 'center', 'color': '#fb4f14', 'fontSize': 30}
                ),
        html.P('new: '+f"{country['total_cases'].iloc[-1] - country['total_cases'].iloc[-2]:,.0f}"
               + ' ('+ str(round(((country['total_cases'].iloc[-1] - country['total_cases'].iloc[-2]) /
                     country['total_cases'].iloc[-1])*100,2)) + '%)',
                           style={
                               'textAlign':'center',
                               'color':'#808080',
                               'fontSize':15,
                               'margin-top': '-18px'

                           })],
),
    #total deaths
html.Div([
        html.H5(children='Total Deaths ', style={'textAlign': 'center', 'color': 'black', 'fontSize': 20}
                 ),
         html.P(f"{country['total_deaths'].iloc[-1]:,.0f}",
                style={'textAlign': 'center', 'color': '#fb4f14', 'fontSize': 30}
                ),
        html.P('new: '+f"{country['total_deaths'].iloc[-1] - country['total_deaths'].iloc[-2]:,.0f}"
               + ' ('+ str(round(((country['total_deaths'].iloc[-1] - country['total_deaths'].iloc[-2]) /
               country['total_deaths'].iloc[-1])*100, 2)) + '%)',
                           style={
                               'textAlign': 'center',
                               'color': '#808080',
                               'fontSize': 15,
                               'margin-top': '-18px'

                           })],),
     # total recovered
html.Div([
        html.H5(children='Total Recoveries ', style={'textAlign': 'center', 'color': 'black', 'fontSize': 20}),
         html.P(f"{country['cumulative recovered'].iloc[-1]:,.0f}",
                style={'textAlign': 'center', 'color': '#fb4f14', 'fontSize': 30}
                ),
        html.P('new: '+f"{country['cumulative recovered'].iloc[-1] - country['cumulative recovered'].iloc[-2]:,.0f}"
               + ' ('+ str(round(((country['cumulative recovered'].iloc[-1] - country['cumulative recovered'].iloc[-2]) /
                     country['total_deaths'].iloc[-1])*100,2)) + '%)',
                           style={
                               'textAlign':'center',
                               'color':'#808080',
                               'fontSize':15,
                               'margin-top': '-18px'

                           })
],),],className="grid-container"),],),

    html.Div([
html.Div([

            dcc.Graph(
               id="pie_fatality",
                config={"displayModeBar": False},

                figure = go.Figure(data=[go.Pie(values=[value_confirmed,value_remain],hole=.9,textinfo="none", hoverinfo='none',showlegend=False, rotation=3)], layout = go.Layout(
  margin=go.layout.Margin(
        l=20, #left margin
        r=1, #right margin
        b=0, #bottom margin
        t=1, #top margin
    ),
                    piecolorway=('#9caf9f','#0B2183'),
                    annotations=[ dict(text=' '+ str (value_confirmed) + '% ', x=0.55, y=0.6 ,font_size=15, showarrow=False),dict(text='OF TOTAL CASES', x=0.51, y=0.45, font_size=10, showarrow=False) ],

)),
                style={"height":150,"width":130}
 ),
],
),

html.Div([
        html.H4(children='Fatality Rate ', style={'textAlign': 'center', 'color': 'black','font':'bold','fontSize': 15,'margin-top':'70px'}
                 ),

],),], className="grid-container-copy"),

html.Div([
html.Div([
            dcc.Graph(
               id="pie_recovery",
                config={"displayModeBar": False},

                figure = go.Figure(data=[go.Pie(values=[value_confirmed2,value_remain2],hole=.9,textinfo="none",hoverinfo='none', showlegend=False, rotation=45 )], layout = go.Layout(
  margin=go.layout.Margin(
        l=20, #left margin
        r=1, #right margin
        b=0, #bottom margin
        t=1, #top margin
    ),
                    piecolorway=('#0B2183','#9caf9f'),
    annotations=[ dict(text=' '+ str (value_confirmed2) + '% ', x=0.55, y=0.6 ,font_size=15, showarrow=False),dict(text='OF TOTAL CASES', x=0.51, y=0.45, font_size=10, showarrow=False) ],

)),
                style={"height":150,"width":130}
 ),
],
),

html.Div([
        html.H4(children='Recovery Rate ', style={'textAlign': 'center', 'color': 'black','font':'bold','fontSize': 15,'margin-top':'70px'}
                 ),

],),


        ], className="grid-container2"),


 ],className="grid-container-total" ),

html.Div([
    html.Div([
        html.Div([
html.H4(children='Past 14 Days Chart ', style={'textAlign': 'left', 'color': 'black', 'fontSize': 20, 'margin-left':'20px', 'margin-bottom':'0px'}
                 ),
                html.Div(

                    children=dcc.Graph(
                        id="country-cases",
                        config={"displayModeBar": True},
                        figure={
                            'data': [
                                {'x': country['date'].tail(14), 'y': country['new_cases'].tail(14), 'type': 'bar',
                                 'name': 'Daily Cases',},
                                {'x': country['date'].tail(14), 'y': country['new_deaths'].tail(14), 'type': 'bar',
                                 'name': 'Daily Deaths'},
                                {'x': country['date'].tail(14), 'y': country['recovered'].tail(14), 'type': 'bar',
                                 'name': 'Daily Recoveries'},

                            ],
                            'layout': {
                               # 'title': 'Past 14 Days',
                                'barmode': 'stack',
                                "colorway": ["#00008b",'#ff8c00','#056608']
                              #  'font': 'bold'


                            },
                        },
                    ),),],className="grid-container-chart",),

    html.Div([
        html.Div([
html.H4(children='Positivity Rate Over The Past 14 Days in %', style={'textAlign': 'left', 'color': 'black', 'fontSize': 20, 'margin-left':'20px'}
                 ),

            dcc.Graph(
                id="vax",
                config={"displayModeBar": True},

                figure={
                    'data': [
                        {'x': country['date'].tail(14), 'y': country['positive_rate'].tail(14), 'type': 'line', 'color':'rgb(0,0,0)',
                         'name': 'Positivity Rate'},


                    ],
                   'layout': { "colorway": ["#00008b"]}
                     #   {'yaxis':{'linecolor':'rgb(204, 204, 204)',} }


                },

            ),
        ],
        ),


    ], className="grid-container3"),
],className="grid-container-total2"),]),

html.Div([
    html.Div([
        html.Div([
html.H4(children='Top 10 Counties With Corresponding Cumulative Cases', style={'textAlign': 'left', 'color': 'black', 'fontSize': 20, 'margin-left':'20px', 'margin-bottom':'0px'}
                 ),
                html.Div(

                    children=dcc.Graph(
                        id="county-cases",
                        config={"displayModeBar": True},

                        figure={
                            'data': [
                                {'y': county['County'].head(10), 'x': county['Cumulative Cases'].head(10), 'type': 'bar','color':'00008b',
                                 'name': 'Top Cases',  'orientation': 'h'},
                                     ],
                            'layout': {
                               # 'title': 'Past 14 Days',

                                'barmode': 'stack',
                                "colorway": ["#00008b"],

                            'yaxis':{'categoryorder':'total ascending','color':'black'},

                              #  'font': 'bold'




                            },
                        },
                    ),),],className="grid-container-chart",),

    html.Div([
        html.Div([
html.H4(children='Vaccination Campaigns Per County in % ', style={'textAlign': 'left', 'color': 'black', 'fontSize': 20, 'margin-left':'20px'}
                 ),
            dcc.Dropdown(
                id='values',
                value='Nairobi',
                style={'margin-left':'10px'},
                options=[{'value': x, 'label': x}
                         for x in [
                             'Baringo', 'Bomet', 'Bungoma', 'Busia', 'Elgeyo Marakwet', 'Embu', 'Garissa', 'Homa Bay', 'Isiolo', 'Kajiado', 'Kakamega', 'Kericho', 'Kiambu', 'Kilifi', 'Kirinyaga', 'Kisii', 'Kisumu', 'Kitui', 'Kwale', 'Laikipia','Lamu','Machakos','Makueni','Mandera','Marsabit','Meru','Migori','Mombasa','Muranga','Nairobi','Nakuru','Nandi','Narok','Nyamira','Nyandarua','Nyeri','Samburu','Siaya','Taita Taveta','Tana River','Tharaka Nithi','Trans Nzoia','Turkana','Uasin Gishu','Vihiga','Wajir','West Pokot']],
                clearable=False
            ),
            dcc.Graph(id="pie-chart"),
        ],
        ),


    ], className="grid-container3"),
],className="grid-container-total2"),])
    #end of app layout
])
@app.callback(
    Output("pie-chart", "figure"),
    [Input("values", "value")])
def generate_chart(values):
   # night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)']


    fig = px.pie(county_vaccinated,values=values,labels='none', names=['Fully Vaccinated', 'Partly Vaccinated', 'Unvaccinated'], color_discrete_sequence=px.colors.sequential.haline)
    fig.update_traces(hoverinfo='none'),
    return fig


if __name__ == '__main__':
     app.run_server(debug=True, port=8080)
