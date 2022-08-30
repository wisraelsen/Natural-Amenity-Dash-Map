# from jupyter-dash_amenities_map_v11_add_forest_data notebook

from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output #, State
import plotly.express as px
import pandas as pd
import json

# load geoJSON counties data
with open('./assets/geojson-counties-fips.json') as fp:
    counties = json.load(fp)

# loading dataframe csv to pandas df, convert to string to keep leading zeros in FIPS codes
df_data = pd.read_csv('./assets/data_table_for_AWS_v1.csv', converters={'FIPS': lambda x: str(x)})

# dicts for colorbar titles and variable descriptions

title_dict = {'Natural_Amenity_Rank':'<----Less Desirable----|     <b>Natural Amenity Rank</b>     |----More Desirable---->',
              'Standardized_Jan_Temp':'<----Colder----|     <b>Winter Temperature</b>     |----Warmer---->',
              'Standardized_Jan_Sun':'<----Less----|     <b>Sun in Winter</b>     |----More---->',
              'Standardized_Jul_Temp':'<----Hotter----|     <b>Summer Temperature</b>     |----Cooler---->',
              'Standardized_Jul_Hum':'<----More Humid----|     <b>Summer Humidity</b>     |----Less Humid---->',
              'Standardized_LN_Water':'<----Less----|     <b>Water Area</b>     |----More---->',
              'Standardized_Topog':'<----Less----|     <b>Topographic Variation</b>     |----More---->',
              'Rural-urban_continuum':'<----More Urban----|     <b>Rural-Urban Continuum</b>     |----More Rural---->',
              'Urban_influence':'<----More----|     <b>Urban Influence</b>     |----Less---->',
              'Snow_Prob': '<----Lesser Chance----|     <b>Snow on Christmas</b>     |----Greater Chance---->',
              'Forest_Percent': '<----Less----|     <b>Forest Area</b>     |----More---->'
             }

description = {'Natural_Amenity_Rank':dcc.Markdown('''***Natural Amenity Rank*** is a composite of six
                    standardized inputs, which can be selected individually, above. Those variables are: January Average Temp, January
                    Sunlight Hours, July Average Temp, July Humidity, Water Area of the county (log scaled), and the amount of
                    Topographical Variation (i.e, mountains vs. plains on a standard scale). The raw data and paper can be found
                    [here](https://www.ers.usda.gov/data-products/natural-amenities-scale/). (*Natural Amenities Drive Rural Population
                    Change*, by David A. McGranahan -- USDA)
                    '''),
              'Standardized_Jan_Temp':dcc.Markdown('''***Winter Temperature*** is the z-score of the average temperature in January by
                    county. This variable was used to obtain the USDA Natural Amenity Rank. The raw data and paper can be found
                    [here](https://www.ers.usda.gov/data-products/natural-amenities-scale/). (*Natural Amenities Drive Rural Population
                    Change*, by David A. McGranahan -- USDA)
                    '''),
              'Standardized_Jan_Sun':dcc.Markdown('''***Sun in Winter*** is the z-score of the average January days of sun by
                    county. This variable was used to obtain the USDA Natural Amenity Rank. The raw data and paper can be found
                    [here](https://www.ers.usda.gov/data-products/natural-amenities-scale/). (*Natural Amenities Drive Rural Population
                    Change*, by David A. McGranahan -- USDA)
                    '''),
              'Standardized_Jul_Temp':dcc.Markdown('''***Summer Temperature*** is the z-score of the average temperature in July by
                    county. This variable was used to obtain the USDA Natural Amenity Rank. The raw data and paper can be found
                    [here](https://www.ers.usda.gov/data-products/natural-amenities-scale/). (*Natural Amenities Drive Rural Population
                    Change*, by David A. McGranahan -- USDA)
                    '''),
              'Standardized_Jul_Hum':dcc.Markdown('''***Summer Humidity*** is the z-score of July humidity data by
                    county. This variable was used to obtain the USDA Natural Amenity Rank. The raw data and paper can be found
                    [here](https://www.ers.usda.gov/data-products/natural-amenities-scale/). (*Natural Amenities Drive Rural Population
                    Change*, by David A. McGranahan -- USDA)
                    '''),
              'Standardized_LN_Water':dcc.Markdown('''***Water Area*** is the z-score of the natural log of the proportion of the county
                    that is water area. This variable was used to obtain the USDA Natural Amenity Rank. The raw data and paper can be found
                    [here](https://www.ers.usda.gov/data-products/natural-amenities-scale/). (*Natural Amenities Drive Rural Population
                    Change*, by David A. McGranahan -- USDA)
                    '''),
              'Standardized_Topog':dcc.Markdown('''***Topographic Variation*** is the z-score of a standard measure of topography by
                    county. This variable was used to obtain the USDA Natural Amenity Rank. The raw data and paper can be found
                    [here](https://www.ers.usda.gov/data-products/natural-amenities-scale/). (*Natural Amenities Drive Rural Population
                    Change*, by David A. McGranahan -- USDA)
                    '''),
              # 'Rural-urban_continuum':'<----More Urban----|     <b>Rural-Urban Continuum</b>     |----More Rural---->',
              'Urban_influence':dcc.Markdown('''***Urban Influence*** is a measure of county population size and proximity to
                    areas of high population. Less *Urban Influence* might contribute positively to the perception of natural
                    amenities. These data are part of the USDA Natural Amenities dataset, but were not used in the Natural Amenity
                    Rank calculations. The raw data and paper can be found
                    [here](https://www.ers.usda.gov/data-products/natural-amenities-scale/). (*Natural Amenities Drive Rural Population
                    Change*, by David A. McGranahan -- USDA)
                    '''),
              'Snow_Prob': dcc.Markdown('''***Chance of White Christmas*** is the probability of snow depth >= 1 inch on Christmas Day,
                    according to 1991-2020 Climate Normals data from the NOAA NCEI. The weather station coordinates from the
                    [raw data](https://www.ncei.noaa.gov/media/3501) were mapped to county FIPS codes using the [FCC API]
                    (https://geo.fcc.gov/api/census/) and averaged if more than one station was available per county. For counties
                    with no station data, probabilities were interpolated from neighboring counties using the US Census Bureau
                    [County Adjacency File](https://www.census.gov/geographies/reference-files/2010/geo/county-adjacency.html).
                    Details are available on [Github](https://github.com/wisraelsen/Natural-Amenity-Dash-Map).
                    '''),
              'Forest_Percent': dcc.Markdown('''***Forest Area*** is the percentage of the county that is forest land, as determined from
                    current US Forest Service Forest Inventory and Analysis (FIA) data retrieved using [EVALIDator 2.0.3]
                    (https://www.fs.usda.gov/ccrc/tool/forest-inventory-data-online-fido-and-evalidator) in 2022. This measure is inclusive
                    of many types of forest – including, for example, mesquite and juniper/pine forest in central and west Texas – and
                    is meant to capture the natural amenity of local tree cover and not just timberland. Details are available on [Github]
                    (https://github.com/wisraelsen/Natural-Amenity-Dash-Map).''')
              }

hover_text_names = {'Natural_Amenity_Rank':'Natural Amenity Rank',
                    'Standardized_Jan_Temp':'Winter Temperature<br>Score',
                    'Standardized_Jan_Sun':'Sun in Winter<br>Score',
                    'Standardized_Jul_Temp':'Summer Temperature<br>Score',
                    'Standardized_Jul_Hum':'Summer Humidity<br>Score',
                    'Standardized_LN_Water':'Water Area<br>Score',
                    'Standardized_Topog':'Topographic Variation<br>Score',
                    'Urban_influence':'Urban Influence<br>Score',
                    'Snow_Prob':'Chance of White Christmas<br>Percent',
                    'Forest_Percent':'Forest Area<br>Percent'
                   }

app = Dash(__name__, external_stylesheets=['bWLwgP.css'])
application = app.server
app.title = "Interactive Natural Amenity Map"

app.layout = html.Div(
    id="map-container",
    children=[
        html.Div(
            id="choropleth-map",
            children=[
            dcc.Graph(id="county-choropleth", style={'height': '98vh'})
            ], className='eight columns'
        ),
        html.Div(
            id='selection-area',
            children=[
                dcc.Markdown('''
                ###### **Where do you want to live?**
                Explore natural amenities by county for the Lower 48 States. This map shows data from multiple public sources,
                including the [USDA ERS Natural Amenities Scale](https://www.ers.usda.gov/data-products/natural-amenities-scale/),
                as well as additional data sets I have retrieved and processed. Higher on the scale (more yellow) would be
                considered 'more desirable' by most people. See below for descriptions and individual data sources.
                '''),
                html.Hr(style = {'margin-top':'1rem', 'margin-bottom':'1rem', 'border-width':'1'}),
                dcc.RadioItems(
                    id='select-variable',
                    options=[
                        {'label':html.B('USDA Natural Amenity Rank'), 'value':'Natural_Amenity_Rank'},
                        {'label':'....Winter Temperature', 'value':'Standardized_Jan_Temp'},
                        {'label':'....Sun in Winter', 'value':'Standardized_Jan_Sun'},
                        {'label':'....Summer Temperature', 'value':'Standardized_Jul_Temp'},
                        {'label':'....Summer Humidity', 'value':'Standardized_Jul_Hum'},
                        {'label':'....Water Area', 'value':'Standardized_LN_Water'},
                        {'label':'....Topographic Variation', 'value':'Standardized_Topog'},
                        {'label':html.B('Urban Influence'), 'value':'Urban_influence'},
                        {'label':html.B('Chance of White Christmas'), 'value':'Snow_Prob'},
                        {'label':html.B('Forest Area'), 'value':'Forest_Percent'}
                    ],
                    value='Natural_Amenity_Rank',),
                html.Center(html.Button('Reset Zoom', id='reset-zoom', n_clicks=0, style = {'height':'30px', 'line-height':'30px'})), # original button is 38px
                html.Hr(style = {'margin-top':'1rem', 'margin-bottom':'1rem', 'border-width':'1'}),
#                 html.P(children=html.B('Data Information'),),
                html.Div(id='variable-description'),
            ], className='four columns', style = {'margin-left':'2%'}
        )
    ],
    className='row',
    style={'backgroundColor':'WhiteSmoke'}  #WhiteSmoke
)
# try making the figure before the callbacks
#   include parameters that don't change
fig = px.choropleth_mapbox(data_frame=df_data,
                           geojson=counties,
                           locations=df_data['FIPS'],
#                            custom_data = df_data[['Hover_county_name','Natural_Amenity_Rank']],
#                            hover_template = "<b>%{customdata[0]}</b><br>%{hover_text_names['Natural_Amenity_Rank']}: %{customdata[1]:.3f}",
                           color=df_data['Natural_Amenity_Rank'],
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=3,
                           center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )
fig.update_traces(customdata = df_data[['Hover_county_name','Natural_Amenity_Rank']], hovertemplate = "<b>%{customdata[0]}</b><br>"+hover_text_names['Natural_Amenity_Rank']+" = %{customdata[1]:.2f}")

fig.update_coloraxes(colorbar_title_side="top") # https://plotly.com/python/reference/layout/coloraxis/
fig.update_coloraxes(colorbar_orientation='h')
fig.update_coloraxes(colorbar_title_text=title_dict['Natural_Amenity_Rank'])
fig.update_coloraxes(colorbar_ypad=25)
fig.update_coloraxes(colorbar_y=-0.1)
fig.update_coloraxes(colorbar_bgcolor="WhiteSmoke")

fig.update_layout(
    autosize=True,
    margin=dict(
    l=0,
    r=0,
    b=0,
    t=0,
    pad=0
    ),
    paper_bgcolor="WhiteSmoke"   #   "LightSteelBlue",
)


@app.callback(
    Output(component_id='variable-description', component_property='children'),
    Input("select-variable","value"),
)
    
def update_variable_div(variable):
    return description[variable]

@app.callback(
    Output("county-choropleth", "figure"),
    Input("select-variable", "value"),
    Input("reset-zoom", "n_clicks"),
)

def update_map(variable, click):  # have to have the outside if/else because this won't work with just using fig['layout']['uirevision'] = "initial" = click = 0, for some reason that I don't understand
    if click == 0:
        fig['layout']['uirevision'] = "initial"  # set first to not change zoom on first input
    
        if ctx.triggered_id == 'select-variable': # keep zoom & center when updating the map variable
            fig['layout']['uirevision'] = "initial"  # keep constant to not change the user-inputted zoom and center
            fig.update_coloraxes(colorbar_title_text=title_dict[variable])  # change colorbar title
            fig.update_traces(z=df_data[variable],
                              selector=dict(type='choroplethmapbox'),
                              customdata = df_data[['Hover_county_name',variable]],
                              hovertemplate = "<b>%{customdata[0]}</b><br>"+hover_text_names[variable]+" = %{customdata[1]:.2f}")  # change map color (z is "color")
        elif ctx.triggered_id == 'reset-zoom':  # reset zoom and center upon button press, only works before we press
            fig['layout']['uirevision'] = click  # change every time with number of clicks to allow change of zoom & center
    else:
        fig['layout']['uirevision'] = click  # set first to not change zoom on first input
        if ctx.triggered_id == 'select-variable': # keep zoom & center when updating the map variable
            fig['layout']['uirevision'] = click  # keep constant to not change the user-inputted zoom and center
            fig.update_coloraxes(colorbar_title_text=title_dict[variable])  # change colorbar title
            customdata = df_data[['Hover_county_name',variable]]
            fig.update_traces(z=df_data[variable],
                              selector=dict(type='choroplethmapbox'),
                              customdata = df_data[['Hover_county_name',variable]],
                              hovertemplate = "<b>%{customdata[0]}</b><br>"+hover_text_names[variable]+" = %{customdata[1]:.2f}")  # change map color (z is "color")
        elif ctx.triggered_id == 'reset-zoom':  # reset zoom and center upon button press, only works before we press
            fig['layout']['uirevision'] = click  # change every time with number of clicks to allow change of zoom & center
        
    return fig

if __name__ == "__main__":
     # Setting debug to True enables debug output. This line should be
     # removed before deploying a production app.
     #application.debug = True
    application.run()  # run the server for AWS
