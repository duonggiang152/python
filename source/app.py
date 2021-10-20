import dash
import dash_table
from dash.html.Br import Br
import dash_bootstrap_components as dbc  # bootstrap for dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from get_covid_data import *

# ---------------------
# Get data
today, total_data_df, today_data_df, overview_7days_df, city_data_df = get_vietnam_covid_data()

# Run the app
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SANDSTONE], update_title='Đang tải...')
app.title = "COVID-19 Dashboard"

# -----------------
#   layout
# -----------------
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

    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=city_data_df.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in city_data_df.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_header={
                        'backgroundColor': 'pink',
                        'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'name'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'death'},
                 'width': '14%', 'textAlign': 'left'},
                {'if': {'column_id': 'treating'},
                 'width': '14%', 'textAlign': 'left'},
                {'if': {'column_id': 'cases'},
                 'width': '14%', 'textAlign': 'left'},
                {'if': {'column_id': 'recovered'},
                 'width': '14%', 'textAlign': 'left'},
                {'if': {'column_id': 'casesToday'},
                 'width': '14%', 'textAlign': 'left'},
            ],
        ),
    ])

])
if __name__ == "__main__":
    app.run_server(debug=True)
