import pandas as pd  # organize the data
import plotly.express as px

#Handle the data
df=pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')
dff=df[['iso_code','location','total_cases','people_fully_vaccinated_per_hundred']].copy().sort_values(by=['total_cases'],ascending=False)
dff.reset_index(inplace=True)
dff=dff.rename(columns = {'people_fully_vaccinated_per_hundred':'Vaccinated rate','total_cases':'Cases'}, inplace = False)


def map_world():
    """Return a graph about number of global covid-19 cases """"


    fig=px.choropleth(data_frame=dff,locations='iso_code',locationmode='ISO-3',
                        color='Cases',
                        hover_data=['location','Cases','Vaccinated rate'],
                        color_continuous_scale="mint",
                        color_continuous_midpoint=1000000,
                        range_color=[0,50000000],
                        labels={'WORLD COVID-19 CASES MAP'},
                        template='plotly')
    return fig
def table_world():
    
    