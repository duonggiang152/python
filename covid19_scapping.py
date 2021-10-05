import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import plotly.express as px
import dash
from dash import dcc
URL = "https://covidmaps.hanoi.gov.vn/"


def get_data():
    lst = []
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="list-statistic2")
    elements=results.find_all("div",class_="item-box")
    for element in elements:
        tmp={}
        location=element.find("div",class_="title-region")
        numbers=element.find("div",class_="val-region")
        tmp["location"]=location.text.strip()
        tmp["numbers"]=int(numbers.text.strip())+50
        lst.append(tmp)
    df=pd.DataFrame.from_records(lst)
    plot_df(df)

def plot_df(df):
    bar_graph=px.bar(data_frame=df,x="location",y='numbers',title="Numbers of COVID cases in Ha Noi",color="location")
    app = dash.Dash(__name__)
    app.layout=dcc.Graph(id="hanoi_cases", figure=bar_graph)
    if __name__ == '__main__':
        app.run_server(debug=True)

get_data()

# while True:
#     get_data()
#     time.sleep(10)
