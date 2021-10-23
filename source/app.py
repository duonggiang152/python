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
                style_data_conditional=[],
                style_header={
                    'backgroundColor': '#CCE2CB',
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
            dcc.Graph(id='barchart-s2'),
            html.Div(id='piechart-s2'),
        ]),

    ])

], className="main")

# ---------------
#checklist -> datatable -> barchart(highlight)
@app.callback(
    [Output('datatable-s2', 'data'), 
        Output('barchart-s2', 'figure')
    ],
    [Input('continent-checklist', 'value'), 
        Input('bar-dropdown-s2', 'value'),
        Input('datatable-s2', 'derived_virtual_selected_rows'),
    ]
)
def update_value(continent_selected, barchart_property, slctd_row_indices,):
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
        template='seaborn',
    )
    
    barchart.update_layout(yaxis={'categoryorder':'total ascending'})
    if slctd_row_indices != None:
        colors = ['#FF0000' if i in slctd_row_indices else '#0074D9'
                for i in range(len(barchart_data))]
        barchart.update_traces(marker_color=colors)

    return (data, barchart)
#datatable highlight selected_row -> barchart highlight -> piechart country
@app.callback(
    [   Output('datatable-s2', 'style_data_conditional'), 
        Output('piechart-s2', 'children'),
    ],
    [   Input('datatable-s2', 'derived_viewport_selected_rows'),
        Input('datatable-s2', 'derived_virtual_data'),
        Input('datatable-s2', 'derived_virtual_selected_rows'),
    ]
)
def highlight_selectedRow(chosen_rows, all_rows_data, slctd_row_indices,):
    #highlight selected row datatable
    style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                },
                {
                    'if': {'row_index': chosen_rows},
                    'backgroundColor': '#D4F0F0'
                },
            ]
    #piechart
    dff = pd.DataFrame(all_rows_data)
    if not slctd_row_indices:
        slctd_row_indices = [0]
    
    country_name = dff.iloc[slctd_row_indices[0]]['location']
    
    country_data = world_data[world_data['location'] == country_name][['location', 'population', 'people_fully_vaccinated', 'people_vaccinated']]
    country_data.index = [0]
    country_data['not_vaccinated'] = country_data['population'] - country_data['people_fully_vaccinated'] - country_data['people_vaccinated']
    country_data = country_data.T.reset_index()
    piechart_data = country_data[2:]
    if piechart_data.loc[2, 0] == None or piechart_data.loc[3, 0] == None or piechart_data.loc[4, 0] == None:
        value = "Không có số liệu"
    elif piechart_data.loc[2, 0] > 0 and piechart_data.loc[3, 0] > 0 and piechart_data.loc[4, 0] > 0:
        piechart_data.replace(to_replace="not_vaccinated", value="Chưa tiêm vaccine", inplace=True)
        piechart_data.replace(to_replace="people_fully_vaccinated", value="Đã tiêm hai mũi", inplace=True)
        piechart_data.replace(to_replace="people_vaccinated", value="Đã tiêm 1 mũi vaccine", inplace=True)
        piechart_data.rename(columns={"index": "Trạng thái", 0: "Số người"}, inplace=True)
        value = dcc.Graph(
                figure = px.pie(data_frame= piechart_data, names='Trạng thái', values='Số người',
                                hole=0.3,
                        ),
                )
    else: value = "Không đủ số liệu"

    return (style_data_conditional, value)

# -------------------------------
# run server
if __name__ == "__main__":
    app.run_server(debug=True)
