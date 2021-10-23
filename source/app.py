# --------------------
import dash
from dash.html.Br import Br
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
# -----------------
# import module & data
from map_world import *
from get_covid_data import *
# -----------------

# Get data
today, total_data_df, today_data_df, overview_7days_df, city_data_df = get_vietnam_covid_data()
world_data = get_world_covid_data()
# ---------------------

# Run the app
app = dash.Dash(__name__, title='COVID-19 Dashboard',
                     update_title='Đang tải...')

# dash layout
app.layout = html.Div([
    #  title page
    html.H1("Thông tin COVID 19", className="title-page"),
    # -------------
    #  Section 1
    html.Section([
        html.Div([html.H2("World Map"),
                  map_world()
                  ], className="graph"),
    ], className="box-1"),

    # --------------
    # Section 2
    html.Div([
        # dropdown continent
        html.Div([
            dcc.Checklist(
                id='continent-checklist',
                options=[
                    {'label': i, 'value': i} for i in ['Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania']
                ],
                value=['Asia'],
                className='my_box_container',
                inputClassName='my_box_input',
                labelClassName='my_box_label'
            )
        ]),
        # Datatable
        html.Div([
            dash_table.DataTable(
                id='datatable-s2',
                data=[{}],
                columns=[
                    {"name": 'Châu lục', "id": 'continent',
                     "deletable": False, "selectable": False},
                    {"name": 'Quốc gia', "id": 'location',
                     "deletable": False, "selectable": False},
                    {"name": 'Số ca nhiễm', "id": 'total_cases',
                     "deletable": False, "selectable": False},
                    {"name": 'Tử vong', "id": 'total_deaths',
                     "deletable": False, "selectable": False},
                    {"name": 'Đã tiêm vaccine', "id": 'people_vaccinated',
                     "deletable": False, "selectable": False},
                    {"name": 'Cập nhật', "id": 'last_updated_date',
                     "deletable": False, "selectable": False},
                ],
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                row_selectable="single",
                row_deletable=False,
                page_action="native",
                page_current=0,
                page_size=7,
                fixed_rows={'headers': True, 'data': 0},
                virtualization=True,
                # style_cell={'textAlign': 'left'},
                style_cell_conditional=[
                    {'if': {'column_id': 'location'},
                     'width': '10%', 'textAlign': 'center'},
                    {'if': {'column_id': 'continent'},
                     'width': '5%', 'textAlign': 'center'},
                    {'if': {'column_id': 'total_cases'},
                     'width': '25%', 'textAlign': 'center'},
                    {'if': {'column_id': 'total_deaths'},
                     'width': '25%', 'textAlign': 'center'},
                    {'if': {'column_id': 'last_updated_date'},
                     'width': '10%', 'textAlign': 'center'},
                    {'if': {'column_id': 'people_vaccinated'},
                     'width': '25%', 'textAlign': 'center'},
                ],
                style_data_conditional=[
                    # {
                    #     'if': {'row_index': 'odd'},
                    #     'backgroundColor': 'rgb(220, 220, 220)',
                    # }
                ],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                }
            )
        ]),
        html.Div([
            dcc.Dropdown(id='bar-dropdown-s2',
                         options=[
                             {'label': 'Số ca nhiễm / triệu dân',
                              'value': 'total_cases_per_million'},
                             {'label': 'Ca tử vong / triệu dân',
                              'value': 'total_deaths_per_million'},
                             {'label': 'Đã tiêm vaccine (ít nhất 1 mũi) / triệu dân',
                              'value': 'people_vaccinated_per_hundred'},
                         ],
                         value='total_cases_per_million',
                         multi=False,
                         clearable=False
                         ),
            dcc.Graph(id='barchart-s2')
        ]),

    ])

], className="main")

# ---------------
#checklist-datatable-barchart
@app.callback(
    [Output('datatable-s2', 'data'), Output('barchart-s2', 'figure')],
    [Input('continent-checklist', 'value'), Input('bar-dropdown-s2', 'value')]
)
def update_value(continent_selected, barchart_property):
    # Get data
    df_filtered = world_data[world_data['continent'].isin(continent_selected)]
    df_filtered.index = [i for i in range(len(df_filtered))]
    # table-data
    data = df_filtered[['location', 'continent', 'total_cases', 'total_deaths',
                        'last_updated_date', 'people_vaccinated']].to_dict('records')
    # barchart
    barchart_data = df_filtered[['location', barchart_property]]
    barchart = px.bar(
        data_frame=barchart_data,
        y='location', 
        x=barchart_property,
        orientation='h',
        labels={"location":"Quốc gia",
                "total_cases_per_million":"Số ca nhiễm / triệu dân",
                "people_vaccinated_per_hundred" : "Đã tiêm vaccine (ít nhất 1 mũi) / triệu dân",
                "total_deaths_per_million":"Ca tử vong / triệu dân"},
        template='ggplot2',
    )
    
    barchart.update_layout(yaxis={'categoryorder':'total ascending'})

    return (data, barchart)
#datatable highlight selected_row
@app.callback(
    Output('datatable-s2', 'style_data_conditional'),
    [Input('datatable-s2', 'derived_viewport_selected_rows'),]
)
def highlight_selectedRow(chosen_rows):
    style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                },
                {
                    'if': {'row_index': chosen_rows},
                    'backgroundColor': 'rgb(252, 164, 214)'
                },
            ]
    return style_data_conditional

# -------------------------------
# run server
if __name__ == "__main__":
    app.run_server(debug=True)
