import pandas as pd  # organize the data
import plotly.express as px
import requests
df=pd.read_html('https://www.statista.com/statistics/1103568/vietnam-coronavirus-cases-by-region/')[0]
vietnam_geojson = requests.get("https://data.opendevelopmentmekong.net/geoserver/ODMekong/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=ODMekong%3Aa4eb41a4-d806-4d20-b8aa-4835055a94c8&outputFormat=application%2Fjson").json()

def map_vietnam():
    """Return a graph about number of covid-19 cases in Vietnam"""

    #Rename some province to match data
    df.loc[df['Characteristic']=='Ho Chi Minh City','Characteristic']='TP. Ho Chi Minh'
    df.loc[df['Characteristic']=='Phu-Tho','Characteristic']='Phu Tho'
    df.loc[df['Characteristic']=='Thua Thien Hue','Characteristic']='Thua Thien - Hue'
    df.loc[df['Characteristic']=='Ben tre','Characteristic']='Ben Tre'


    #Plot the graph
    fig=px.choropleth(data_frame=df,
                        geojson=vietnam_geojson,locations='Characteristic',featureidkey="properties.Name_EN",
                        color='Number of cases',
                        hover_data=['Number of cases'],
                        color_continuous_scale="mint",
                        labels={'VIETNAM COVID-19 CASES MAP'},
                        template='plotly')
    return fig
    
