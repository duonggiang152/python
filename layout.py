import dash
from dash.html.Br import Br
import dash_bootstrap_components as dbc  # bootstrap for dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Run the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], update_title='Đang tải...')
app.layout = html.Div([
    # Row 1: Title(co the sua thanh navbar)
    dbc.Row(dbc.Col(html.H1("Thông tin COVID"),
                    width={'size': True},
                    style={'text-align': 'center'}
                    ),
            ),
    # Row 2: Map va cot thong tin
    dbc.Row([
        dbc.Col(dcc.Graph(id='map', figure={}),
                width={'size': 8, "offset": 2},
                style={'background-color': 'red'}
                ),
        dbc.Col(html.H3("Information here"),
                width=2,
                style={'background-color': 'pink'})
    ]),
    # Row 3: Bieu do 1
    dbc.Row(
        [
            html.H2("Bieu do 1"),
            dbc.Col(dcc.Dropdown(id='drop-1', placeholder='dropdown',
                         options=[{'label': 'Option A', 'value': 'optA'},
                                  {'label': 'Option B', 'value': 'optB'}]),
                    width={'size':3}
                    ),
            dbc.Col(dcc.Graph(id='graph-1', figure={}),
                    width={'size': 8, "offset": 2},
                    style={'background-color': 'red'}
                    )
        ], no_gutters=True
    ),
    # Row 4: Bieu do 2
    dbc.Row(
        [
            html.H2("Bieu do 2"),
            dbc.Col(dcc.Dropdown(id='drop-2', placeholder='dropdown',
                         options=[{'label': 'Option A', 'value': 'optA'},
                                  {'label': 'Option B', 'value': 'optB'}]),
                    width={'size':3}
                    ),
            dbc.Col(dcc.Graph(id='graph-2', figure={}),
                    width={'size': 8, "offset": 2},
                    style={'background-color': 'red'}
                    )
        ], no_gutters=True
    ),
    # Row 5: Bieu do 3
    dbc.Row(
        [
            html.H2("Bieu do 3"),
            dbc.Col(dcc.Dropdown(id='drop-3', placeholder='dropdown',
                         options=[{'label': 'Option A', 'value': 'optA'},
                                  {'label': 'Option B', 'value': 'optB'}]),
                    width={'size':3}
                    ),
            dbc.Col(dcc.Graph(id='graph-3', figure={}),
                    width={'size': 8, "offset": 2},
                    style={'background-color': 'red'}
                    )
        ], no_gutters=True
    ),
    # Row 6: Bieu do 4
    dbc.Row(
        [
            html.H2("Bieu do 4"),
            dbc.Col(dcc.Dropdown(id='drop-4', placeholder='dropdown',
                         options=[{'label': 'Option A', 'value': 'optA'},
                                  {'label': 'Option B', 'value': 'optB'}]),
                    width={'size':3}
                    ),
            dbc.Col(dcc.Graph(id='graph-4', figure={}),
                    width={'size': 8, "offset": 2},
                    style={'background-color': 'red'}
                    )
        ], no_gutters=True
    )
])
if __name__ == "__main__":
    app.run_server(debug=True)
