from dash import html
from get_covid_data import get_vietnam_covid_data
def render_Box_Covid_VN():
    """
    tra ve chuoi html element dua tren dash layout
    ve cac ca nhiem tren dia ban cac tinh o viet nam
    kieu tra ve list
    """
    #  get dataFrame
    (today, total_data_df, today_data_df, overview_7days_df, city_data_df) = get_vietnam_covid_data()
    #convert datafram to dist
    data = city_data_df.to_dict(orient= "records")
    listElement = []
    # create list Element
    for i in range(0, len(data)):
        provinceDiv = html.Div(f'{data[i]["name"]}')
        caseDiv     = html.Div(f'{data[i]["cases"]}')
        listElement.append(html.Div([provinceDiv, caseDiv], className = "province-content"))
    return listElement
