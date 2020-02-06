import json

from bs4 import BeautifulSoup
import requests


def get_episode_data(page):
    episode_data = {}
    patient_data = {}

    soup = BeautifulSoup(page.content, 'html.parser')
    data_div = soup.find('div', attrs={'id': "mw-content-text"})
    # = data_div.find_next("h2")
    h2_headline = data_div.find_next("h2")
    while h2_headline is not None:
        if h2_headline.find('span', attrs={'id': "Medical_Notes"}):
            break
        else:
            h2_headline = h2_headline.find_next("h2")
    #print(h2_headline.parent)
    diagnose_h = soup.find(text="Diagnosis:").parent.parent
   # patient_diseases = diagnose_h.find_all("li")
    patient_diagnose = []
    for li in diagnose_h.findAll('li'):
        patient_diagnose.append(li.text.strip())
    #print(patient_diagnose)
    patient_h3 = diagnose_h.parent.previous_sibling.previous_sibling
    patient_link = patient_h3.find('a')
    patient_name = patient_link.attrs['title']
    if patient_link.has_attr('href'):
        patient_url = patient_link.attrs['href']
    print(patient_name)
    print(patient_url)
    #print(type(soup.find(text="Diagnosis:").parent.parent))

    #patient_diseases = [li.text.strip() for ul in diagnose_h for li in diagnose_h.findAll('li')]
   # print(patient_diseases)
    #print(h2_headline.next_sibling.next_element)
    #h3head = h2_headline.next_sibling
    #patient_data['name'] = \
    #print(type(h3head))

    #print(h2_headline.find_next().find_next().find_next().find_next().find_next())
    '''
    temp = h2_headline.find_next()
    print(h2_headline.name)
    print(h2_headline.find_next().next())
    while h2_headline.next().name != 'h2':
        if h2_headline.name == 'h3':
            temp_patient_data = {}
            temp_patient = h2_headline.next()
            temp_patient_data['name'] = temp_patient.find('mw-headline')
            temp_patient_link = temp_patient.find('a')
            if temp_patient_link is not None:
                if temp_patient_link.has_attr('href'):
                    temp_patient_data['patient_link'] = temp_patient.find('a')
        if h2_headline.name == 'ul':
            h2_field = h2_headline.find('b')
            print("whatever")
'''




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
