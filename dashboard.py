from plotly.data import gapminder
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
app = Dash(name="Gapminder Dashboard", external_stylesheets=css)

################### DATASET ####################################
gapminder_df = gapminder(datetimes=True, centroids=True, pretty_names=True)
gapminder_df["Year"] = gapminder_df.Year.dt.year

#################### CHARTS #####################################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=gapminder_df.columns, align='left'),
        cells=dict(values=gapminder_df.values.T, align='left'))
    ]
    )
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0, "l":0, "r":0, "b":0}, height=700)
    return fig

def create_population_chart(continent="Asia", year=1952, ):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="Population", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="Population", color="Country",
                   title="Country {} for {} Continent in {}".format("Population", continent, year),
                   text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="GDP per Capita", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="GDP per Capita", color="Country",
                   title="Country {} for {} Continent in {}".format("GDP per Capita", continent, year),
                   text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="Life Expectancy", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="Life Expectancy", color="Country",
                   title="Country {} for {} Continent in {}".format("Life Expectancy", continent, year),
                   text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_choropleth_map(variable, year):
    filtered_df = gapminder_df[gapminder_df.Year==year]

    fig = px.choropleth(filtered_df, color=variable, 
                        locations="ISO Alpha Country Code", locationmode="ISO-3",
                        color_continuous_scale="RdYlBu", hover_data=["Country", variable],
                        title="{} Choropleth Map [{}]".format(variable, year)
                     )

    fig.update_layout(dragmode=False, paper_bgcolor="#e5ecf6", height=600, margin={"l":0, "r":0})
    return fig

##################### WIDGETS ####################################
continents = gapminder_df.Continent.unique()
years = gapminder_df.Year.unique()

cont_population = dcc.Dropdown(id="cont_pop", options=continents, value="Asia",clearable=False)
year_population = dcc.Dropdown(id="year_pop", options=years, value=1952,clearable=False)

cont_gdp = dcc.Dropdown(id="cont_gdp", options=continents, value="Asia",clearable=False)
year_gdp = dcc.Dropdown(id="year_gdp", options=years, value=1952,clearable=False)

cont_life_exp = dcc.Dropdown(id="cont_life_exp", options=continents, value="Asia",clearable=False)
year_life_exp = dcc.Dropdown(id="year_life_exp", options=years, value=1952,clearable=False)

year_map = dcc.Dropdown(id="year_map", options=years, value=1952,clearable=False)
var_map = dcc.Dropdown(id="var_map", options=["Population", "GDP per Capita", "Life Expectancy"],
                        value="Life Expectancy",clearable=False)

##################### APP LAYOUT ####################################
app.layout = html.Div([
    html.Div([
        html.H1("Gapminder Dataset Analysis", className="text-center fw-bold m-2"),
        html.Br(),
        dcc.Tabs([
            dcc.Tab([html.Br(),
                     dcc.Graph(id="dataset", figure=create_table())], label="Dataset"),
            dcc.Tab([html.Br(), "Continent", cont_population, "Year", year_population, html.Br(),
                     dcc.Graph(id="population")], label="Population"),
            dcc.Tab([html.Br(), "Continent", cont_gdp, "Year", year_gdp, html.Br(),
                     dcc.Graph(id="gdp")], label="GDP Per Capita"),
            dcc.Tab([html.Br(), "Continent", cont_life_exp, "Year", year_life_exp, html.Br(),
                     dcc.Graph(id="life_expectancy")], label="Life Expectancy"),
            dcc.Tab([html.Br(), "Variable", var_map, "Year", year_map, html.Br(),
                     dcc.Graph(id="choropleth_map")], label="Choropleth Map"),
        ])
    ], className="col-8 mx-auto"),
], style={"background-color": "#e5ecf6", "height": "100vh"})

##################### CALLBACKS ####################################
@callback(Output("population", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value"),])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)

@callback(Output("gdp", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value"),])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)

@callback(Output("life_expectancy", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value"),])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)

@callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value"),])
def update_map(var_map, year):
    return create_choropleth_map(var_map, year)

if __name__ == "__main__":
    app.run(debug=True)