import json
import html
from bs4 import BeautifulSoup
import requests


def get_episode_data(page):
    episode_data = {}
    patients_data = {}

    soup = BeautifulSoup(page.content, 'html.parser')
    data_div = soup.find('div', attrs={'id': "mw-content-text"})
    # = data_div.find_next("h2")
    '''
    h2_headline = data_div.find_next("h2")
    while h2_headline is not None:
        if h2_headline.find('span', attrs={'id': "Medical_Notes"}):
            break
        else:
            h2_headline = h2_headline.find_next("h2")
    '''
    diagnose_text = soup.find(text="Diagnosis:")
    treatment_text = soup.find(text="Treatment:")
    while diagnose_text is not None:
        patient_data = {}
        patient_diagnose = []
        patient_treatment = []

        diagnose_h = diagnose_text.parent.parent
        # getting diagnoses
        for li in diagnose_h.findAll('li'):
            patient_diagnose.append(li.text.strip())
        patient_data['diagnose'] = patient_diagnose
        diagnose_text = diagnose_text.find_next(text="Diagnosis:")

        # getting patient
        patient_h3 = diagnose_h.parent.previous_sibling.previous_sibling
        patient_h3_span = patient_h3.find('span', attrs={'class': "mw-headline"})

        patient_link = patient_h3_span.find('a')
        patient_data['name'] = html.unescape(patient_h3_span.attrs['id']).replace("_", " ").replace(".27","'")
        if patient_link and patient_link.has_attr('href'):
            patient_data['patient url'] = patient_link.attrs['href']
        # getting treatment list
        if treatment_text:
            treatment_h = treatment_text.parent.parent
            for li in treatment_h.findAll('li'):
                patient_treatment.append(li.text.strip())
            patient_data['treatment'] = patient_treatment
            treatment_text = treatment_text.find_next(text="Treatment:")
        # iterating to next
        patients_data[patient_data['name']] = patient_data
    return patients_data
    #print(json.dumps(patients_data))

def get_season_from_table(season_table):
    season_dict = []
    episode_dict = {}
    episode_number = 1
    episodes_links = season_table.find_all('a')
    for episode_link in episodes_links:
        if episode_link.has_attr('href'):
            episode_dict = get_episode_data(requests.get('https://greysanatomy.fandom.com/' + episode_link.attrs['href']))
            episode_dict['episode name'] = episode_link.text.strip()
            episode_dict['episode number'] = str(episode_number)
            season_dict.append(episode_dict)
            episode_number += 1
    return season_dict

def greys_data():
    seasons_page = requests.get("https://greysanatomy.fandom.com/wiki/Grey%27s_Anatomy_Episodes")
    seasons_page = BeautifulSoup(seasons_page.content, 'html.parser')
    seasons_tables = seasons_page.find_all('table', attrs={'class': "wikitable plainrowheaders"})
    seasons_dict = {}
    season_number = 1
    for season_table in seasons_tables:
        seasons_dict[season_number] = get_season_from_table(season_table)
        print(seasons_dict[season_number])
        season_number += 1
    print(json.dumps(seasons_dict))
