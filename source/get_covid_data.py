# This Python file uses the following encoding: utf-8
import pandas as pd                         #pip install pandas
import requests                             #pip install requests
from apify_client import ApifyClient        #pip install apify-client


def get_world_covid_data():
    """
    Return a dataframe of COVID data of 45 countries include:
    'infected', 'tested', 'recovered', 'deceased', 'country', 'moreData', 'historyData', 'sourceUrl', 'lastUpdatedApify', 'lastUpdatedSource'
    """
    world_covid_data_dict = {} 
    
    client = ApifyClient("apify_api_k4mBbzZyCQQBGm9bHEMngYQ92RlLFp0t6DPQ")  #APIFY token cua @Manh
    run_input = {}
    run = client.actor("petrpatek/covid-19-aggregator").call(run_input=run_input) #call actor

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        #each item is a dict
        world_covid_data_dict[item.get("country")] = item

    df = pd.DataFrame(world_covid_data_dict)
    return df.T


def get_vietnam_covid_data():
    """
        return 
    """
    response = requests.get("https://static.pipezero.com/covid/data.json")
    vietnam_covid_data_dict = response.json()
    print(vietnam_covid_data_dict.keys())





def main():
    get_vietnam_covid_data()


if __name__ == "__main__":
    main()