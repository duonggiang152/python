# This Python file uses the following encoding: utf-8
import pandas as pd                         
import requests                             
from bs4 import BeautifulSoup               

def get_world_covid_data():
    """
    Return a dataframe of COVID data of 215 countries
    """
    #Source: Our World In Data: "https://github.com/owid/covid-19-data"
    data_requests = requests.get(
        'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.json')

    world_data = dict(data_requests.json())
    df = pd.DataFrame(world_data).T

    return df


def get_vietnam_covid_data():
    """
        Return COVID data of VietNam, world:
            (str)today = today's date\n
            (df)total_data_df: 'death', 'treating', 'cases', 'recovered'  (today_data_df.internal['death'])\n
            (df)today_data_df: 'death', 'treating', 'cases', 'recovered'\n
            (df)overview_7days_df: 'date', 'death', 'treating', 'cases', 'recovered', 'avgCases7day', 'avgRecovered7day', 'avgDeath7day'\n
            (df)city_data_df: 'name','death', 'treating', 'cases', 'recovered', 'casesToday'
    """
    
    #Source: "https://covid19.gov.vn/"
    response = requests.get("https://static.pipezero.com/covid/data.json")
    vietnam_covid_data_dict = response.json()

    total_data_df = pd.DataFrame(vietnam_covid_data_dict['total'])
    today_data_df = pd.DataFrame(vietnam_covid_data_dict['today'])
    overview_7days_df = pd.DataFrame(vietnam_covid_data_dict['overview'])
    today  = overview_7days_df.iloc[-1]['date']
    city_data_df = pd.DataFrame(vietnam_covid_data_dict['locations'])

    return today, total_data_df, today_data_df, overview_7days_df, city_data_df
    
def get_hanoi_covid_data():
    """
        Return a dataframe COVID data of Hanoi ('locations' - 'positive cases')
    """
    lst = []
    page = requests.get("https://covidmaps.hanoi.gov.vn/")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="list-statistic2")
    elements=results.find_all("div",class_="item-box")
    for element in elements:
        tmp={}
        location=element.find("div",class_="title-region")
        numbers=element.find("div",class_="val-region")
        tmp["location"]=location.text.strip()
        tmp["positive"]=int(numbers.text.strip())
        lst.append(tmp)
    df=pd.DataFrame.from_records(lst)
    
    return df

def get_vaccine_data_vietnam_city():
    """
        Return a dataframe Vaccine data Vietnam city
    """
    response = requests.get("https://vnexpress.net/microservice/sheet/type/vaccine_data_map")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")

    return df

def get_vaccine_to_vietnam():
    """
        Return a dataframe Vaccine to Vietnam
    """
    response = requests.get("https://vnexpress.net/microservice/sheet/type/vaccine_to_vietnam")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")

    return df

def get_vaccine_data_vietnam():
    """
        Return a dataframe Vaccine to Vietnam
        df.loc[df["Ngày"][:] == "9/10"]
    """
    response = requests.get("https://vnexpress.net/microservice/sheet/type/vaccine_data_vietnam")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")

    return df 

def main():
    return

if __name__ == "__main__":    
    main()