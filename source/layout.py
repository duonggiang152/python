# import modul from flask

from os import link
from dash.html.Div import Div
from dash.html.H3 import H3
import flask
from flask import Response
#--------------
# import modul from dash

import dash
from dash.html.Br import Br
from dash_extensions import DeferScript
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
# -----------------
#import modul render & data

from get_covid_data import get_vietnam_covid_data
from render_Box_Covid_VN import render_Box_Covid_VN
# -------------
# Create main server

app_flask = flask.Flask(__name__)

#path default css and javascript assets for dash
import os
assets_path = os.getcwd() + './view/home'

# Run the app
app_dash = dash.Dash(__name__,assets_folder=assets_path,server = app_flask, update_title='Đang tải...', url_base_pathname="/")

#dash layout
app_dash.layout = html.Div([
    #  title page
    html.H1("Thông tin COVID 19", className= "title-page"),
    #  1st block
    #  ban do the gioi + data table
    html.Section([
        html.Div([html.H2("Bieu do 1"),
            dcc.Dropdown(id='drop-1', placeholder='dropdown',
                         options=[{'label': 'Option A', 'value': 'optA'},
                                  {'label': 'Option B', 'value': 'optB'}]),
            dcc.Graph(id='graph-1', figure={})], className= "graph"),
        #case detail
        html.Div(render_Box_Covid_VN(), className="box-province")
    ], className = "box-1"),
    # 2nd block
    # bieu do duong ve so ca trong tuan 
    html.Div([
        html.H2("Bieu do 2"),
        dcc.Dropdown(id='drop-2', placeholder='dropdown',


                         options=[{'label': 'Option A', 'value': 'optA'},
                                  {'label': 'Option B', 'value': 'optB'}]),
        dcc.Graph(id='graph-2', figure={})
    ], className = "box3"),
    # 3rd block
    # bieu do tron ty le tiem vac xin so dan chua tiem, tiem mui 1, tiem mui 2
    html.Div([
        html.H2("Bieu do 3"),
        dcc.Dropdown(id='drop-3', placeholder='dropdown',
                         options=[{'label': 'Option A', 'value': 'optA'},
                                  {'label': 'Option B', 'value': 'optB'}]),
        dcc.Graph(id='graph-3', figure={})
    ], className = "box3"),
    # 4th block
    # bieu do cot + so ca chet , location (diaphuong), truc hoanh: so ca
    html.Div([
        html.H2("Bieu do 4"),
        dcc.Dropdown(id='drop-4', placeholder='dropdown',
                         options=[{'label': 'Option A', 'value': 'optA'},
                                  {'label': 'Option B', 'value': 'optB'}]),
        dcc.Graph(id='graph-4', figure={})
    ], className = "box3"),
    html.Div("Cropyright belong to group 3", id = "foodter")
    # DeferScript(src = "./view/home/getData.js")
], className= "main")

# route
@app_flask.route("/data-frist-block")
def dataFristBlock():    
    (today, total_data_df, today_data_df, overview_7days_df, city_data_df) = get_vietnam_covid_data()
    resdata = city_data_df.to_json(orient = 'records')
    return Response(resdata, mimetype="application/json")
# handle event test
@app_dash.callback(
    Output(component_id= "testclick", component_property='children'),
    Input(component_id= "testclick2", component_property="n_clicks"),
    prevent_initial_call = True)
def undate(c):
    print("halo {}".format(c))
    return "halo {}".format(c)
# run server
if __name__ == "__main__":
    app_dash.run_server()
