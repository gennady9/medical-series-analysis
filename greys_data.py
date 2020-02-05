import json

from bs4 import BeautifulSoup
import requests


def get_episode_data(page):
    episode_data = {}
    soup = BeautifulSoup(page.content, 'html.parser')
    data_div = soup.find('div', attrs={'id': "mw-content-text"})
    # = data_div.find_next("h2")
    h2_headline = data_div.find_next("h2")
    while h2_headline is not None:
        if h2_headline.find('span', attrs={'id': "Medical_Notes"}):
            break
        h2_headline = h2_headline.find_next("h2")

    
    temp_patient_data = {}
    while h2_headline.next():
        # patient headline
        temp_patient = h2_headline.next()
        temp_patient_data['name'] = temp_patient.find('mw-headline')
        temp_patient_link = temp_patient.find('a')
        if temp_patient_link is not None:
            if temp_patient_link.has_attr('href'):
                temp_patient_data['patient_link'] = temp_patient.find('a')





def greys_data():
    List_of_patients ={}
    page = requests.get("https://greysanatomy.fandom.com/wiki/In_the_Midnight_Hour")
    patient_data = get_episode_data(page)

    print("blabla")

# code graveyard
#    h2_headlines = data_div.find_next("h2").find_next("h2").find_next("h2").find_next("h2").find_next("h2").find_next("h2").find_next("h2")
# h2_medical = (data_div.content).find_next_sibling("h2")
# h2_headlines = data_div.find_all('h2')
# for h2_headline in h2_headlines:

# print(data_div)
