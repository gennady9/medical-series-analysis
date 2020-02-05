import json

from bs4 import BeautifulSoup
import requests

def get_gender(page):
    gender_soup = BeautifulSoup(page.content, 'html.parser')
    category = gender_soup.find('div', attrs={'class': 'page-header__categories-links'})
    category = category.find_all('a')
    categories = []
    for c in category:
        categories.append(c.text.strip())

    gender = 'Unknown'
    if 'Males' in categories:
        gender = 'Male'
    elif 'Females' in categories:
        gender = 'Female'
    return gender

def get_patient_data(page):
    age = 'Unknown'
    occupation = 'Unknown'
    death = 'Unknown'
    age_soup = BeautifulSoup(page.content, 'html.parser')
    age_table_div = age_soup.find('div', attrs={'id': 'mw-content-text'})
    age_table = age_table_div.find('table')
    if age_table:
        rows = age_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                if cols[0].text.strip() == 'Age':
                    age = cols[1].text.strip()
                if cols[0].text.strip() == 'Occupation':
                    occupation = cols[1].text.strip()
                if cols[0].text.strip() == 'Date of Death':
                    death = cols[1].text.strip()

    return age, occupation, death
############# House Info
def house_data():
    page = requests.get("https://house.fandom.com/wiki/List_of_medical_diagnoses")
    soup = BeautifulSoup(page.content, 'html.parser')

    seasons = {}
    for seasonNumber in range(1, 9):  # season 1 to 8
        seasondiv = soup.find('div', attrs={'title': "Season " + str(seasonNumber)})
        table = seasondiv.find('table', attrs={'class': 'article-table'})
        rows = table.find_all('tr')
        rowId = -1
        episodes = []
        temp_episode_number = 0
        temp_episode_name = 0
        temp_episode_link = 0
        for row in rows:
            rowId += 1
            if rowId == 0:
                continue
            data = {}
            diagnoses = {}

            cols = row.find_all('td')
            if len(cols) < 2:  # avoiding rows with single element
                rowId -= 1
                continue
            if len(cols) == 2:
                diseasesLink = []
                data['patient'] = cols[0].text.strip()
                patientLink = cols[0].find('a')
                if patientLink:
                    if patientLink.has_attr('href'):
                        data['patient_link'] = cols[0].find('a').attrs['href']
                        patient_page = requests.get('https://house.fandom.com/' + data['patient_link'])
                        data['gender'] = get_gender(patient_page)
                        data['age'], data['occupation'], death = get_patient_data(patient_page)
                        if death != 'Unknown':
                            data['death_date'] = death
                data['diagnose'] = cols[1].text.strip()
                iteratingDiseases = cols[1].find_all('a')
                for diseaseLink in iteratingDiseases:
                    if diseaseLink.has_attr('href'):
                        diseasesLink.append(diseaseLink.attrs['href'])
                data['diagnoses_links'] = diseasesLink
                data['episode_number'] = temp_episode_number
                data['episode name'] = temp_episode_name
                data['episode link'] = temp_episode_link
                episodes.append(data)
                seasons[seasonNumber] = episodes
                continue
                # diseasesLink.append(cols[1].text.strip())
            # print(row)
            data['episode_number'] = cols[0].text.strip()
            data['episode name'] = cols[1].text.strip()
            data['episode link'] = cols[1].find('a').attrs['href']
            data['patient'] = cols[2].text.strip()

            data['patient_link'] = cols[2].find('a').attrs['href']
            patient_page = requests.get('https://house.fandom.com/' + data['patient_link'])
            data['gender'] = get_gender(patient_page)
            data['age'], data['occupation'], death = get_patient_data(patient_page)
            if death != 'Unknown':
                data['death_date'] = death

            data['diagnose'] = cols[3].text.strip()
            links = cols[3].find_all('a')
            diseaseLink = []
            for link in links:
                if link.has_attr('href'):
                    diseaseLink.append(link.attrs['href'])
            data['diagnoses_links'] = diseaseLink
            temp_episode_number = data['episode_number']
            temp_episode_name = data['episode name']
            temp_episode_link = data['episode link']
            # print(data)
            episodes.append(data)
        seasons[seasonNumber] = episodes

    json_data = json.dumps(seasons)
    return json_data
    #print(json_data)

### Actors
def get_actor_data(page):
    actor_data = {}
    #age = 'Unknown'
    #occupation = 'Unknown'

    age_soup = BeautifulSoup(page.content, 'html.parser')
    age_table_div = age_soup.find('div', attrs={'id': 'mw-content-text'})
    age_table = age_table_div.find('table')
    if age_table:
        rows = age_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                if cols[0].text.strip() == 'Born':
                    actor_data['birthday'] = cols[1].text.strip()
                if cols[0].text.strip() == 'Birthplace':
                    actor_data['birthplace'] = cols[1].text.strip()
    return actor_data

### Doctors
def get_doctor_data(page):
    doctor_data = {}
    #age = 'Unknown'
    #occupation = 'Unknown'

    age_soup = BeautifulSoup(page.content, 'html.parser')
    age_table_div = age_soup.find('div', attrs={'id': 'mw-content-text'})
    age_table = age_table_div.find('table')
    if age_table:
        rows = age_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                if cols[0].text.strip() == 'Name':
                    doctor_data['name'] = cols[1].text.strip()
                if cols[0].text.strip() == 'Age':
                    doctor_data['age'] = cols[1].text.strip()
                if cols[0].text.strip() == 'Marital Status':
                    doctor_data['marital status'] = cols[1].text.strip()
                if cols[0].text.strip() == 'Occupation':
                    doctor_data['occupation'] = cols[1].text.strip()
                if cols[0].text.strip() == 'Date of Death':
                    doctor_data['death'] = cols[1].text.strip()
                if cols[0].text.strip() == 'Actor':
                    actor_link = cols[1].find('a')
                    if actor_link.has_attr('href'):
                        actor_data = get_actor_data(requests.get('https://house.fandom.com/' + actor_link.attrs['href']))
                    actor_data['actor name'] = cols[1].text.strip()
                    doctor_data['actor'] = actor_data

    return doctor_data

def get_house_doctors():
    page = requests.get("https://house.fandom.com/wiki/House_Wiki")
    soup = BeautifulSoup(page.content, 'html.parser')

    doctor_link_list = []
    doctor_data = {}
    doctors = {}

    doctors_div = soup.find('div', attrs={'class': "lcs-container"})
    doctors_table = doctors_div.find_all('table', attrs={'cellspacing': '4'})
    for doctor_table in doctors_table:
        doctors_links = doctor_table.find_all('a')
        for doctor_link in doctors_links:
            if doctor_link.has_attr('href'):
                doctor_link_list.append(doctor_link.attrs['href'])
    doctor_link_list = list(dict.fromkeys(doctor_link_list))

    for doctor_link in doctor_link_list:
        doctor_page = requests.get('https://house.fandom.com/' + doctor_link)
        doctor_data = get_doctor_data(doctor_page)
        doctor_data['gender'] = get_gender(doctor_page)
        doctors[doctor_data['name']] = doctor_data
