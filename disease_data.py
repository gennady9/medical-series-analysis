import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import json

from bs4 import BeautifulSoup
import requests


gecko_path = "C:/dhp/geckodriver.exe"

def orpha_scrape(link):
    disease_dict = {}
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    #div_block = soup.find("div", {"class": "idcard artBlock"})
    card_list = soup.find("ul", {"class": "idData"})
    em_list = card_list.find_all('em')
    for em in em_list:
        if em.string.strip() == 'Prevalence:':
            disease_dict['prevalence'] = em.next_sibling.string
        elif em.string.strip() == 'Age of onset:':
            disease_dict['age_of_onset'] = em.next_sibling.string
    return disease_dict


def get_all_malacard_data(malacard_link_list):
    new_malacard_list = []
    driver = webdriver.Firefox(executable_path=gecko_path)

    progress_tracking = 0
    diseases_len = len(malacard_link_list)

    for malacard_dict in malacard_link_list:
        # progress tracking
        progress_tracking += 1
        print("[" + str(progress_tracking) + "/" + str(diseases_len) + "]" + "disease = " + malacard_dict['disease'])

        # ignoring diseases without malacard link
        if 'no_match' in malacard_dict['link']:
            new_malacard_list.append(malacard_dict)
            continue

        # loading page
        driver.get(malacard_dict['link'])
        time.sleep(3) # let webpage time to load
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # getting external link of orpha
        external_id_div = soup.find('div', attrs={'id': 'ExternalId'})
        orpha_link = "no_match"
        if external_id_div:
            external_links = external_id_div.find_all('a')
            for link in external_links:
                if 'orpha' in link.text.lower():
                    if link.has_attr('href'):
                        orpha_link = link.attrs['href']
                        break

        # getting orpha data
        orpha_data = {}
        if 'no_match' not in orpha_link:
            orpha_data = orpha_scrape(orpha_link)

        # getting disease group
        category = []
        tab_divs = soup.find_all('div', attrs={'class': 'tab'})
        for tab_div in tab_divs:
            if tab_div.find("b", string="MalaCards categories: "):
                category_links = tab_div.find_all('a')
                for link in category_links:
                    if 'See all' not in link.text:
                        category.append(link.text)
                break
        malacard_dict['orpha_link'] = orpha_link
        malacard_dict['orpha_data'] = orpha_data
        malacard_dict['category'] = category
        new_malacard_list.append(malacard_dict)


    driver.quit()
    return new_malacard_list
    #print(json.dumps(new_malacard_list))


'''
    #url_prefix = 'https://www.malacards.org/search/results?query='
    #urlpage = url_prefix + disease_name
    print(urlpage)

    # get web page
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

        # getting external link of orpha
        external_id_div = soup.find('div', attrs={'id': 'ExternalId'})
        orpha_link = "no_match"
        if external_id_div:
            external_links = external_id_div.find_all('a')
            for link in external_links:
                if 'orpha' in link.text.lower():
                    if link.has_attr('href'):
                        orpha_link = link.attrs['href']
                        break
                        #print(orpha_link)



'''


def get_disease_table_link(disease_list):

    disease_result_list = []
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(executable_path=gecko_path)

    progress = 0
    diseases_len = len(disease_list)

    url_prefix = 'https://www.malacards.org/search/results?query='
    for disease_name in disease_list:
        disease_data = ({"disease": disease_name, "link": "no_match"})
        urlpage = url_prefix + disease_name
        #print(urlpage)
        driver.get(urlpage)
        time.sleep(3)
        match_quality = 0.0
        try:
            match_quality = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/table/tbody/tr[2]/td[7]").text
        except NoSuchElementException:  # spelling error making this code not work as expected
            pass
        if (float(match_quality)) > 1.75:
            result = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/table/tbody/tr[2]/td[5]")
            disease_name = result.text
            link = result.find_element_by_tag_name('a')
            disease_link = link.get_attribute("href")
            # append dict to array
            disease_data = ({"disease": disease_name, "link": disease_link})
        disease_result_list.append(disease_data)
        progress += 1
        print("[" + str(progress) +"/" + str(diseases_len) + "]" + "disease = " + disease_name)
    driver.quit()
    return disease_result_list
    #return disease_data
    #
    #    print(soup)
    # print("bla")

'''
def get_all_disease_data(disease_table):
    not_found = 0
    data = []
    for disease in disease_table:
        current_data = get_disease_data(disease)
        if current_data == "no match":
            not_found += 1
        else:
            print(current_data)
            data.append(current_data)
    return data
    
    
    
    # structure with disease name
def get_disease_table_link(disease_list):

    disease_result_list = []
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(executable_path=gecko_path)

    progress = 0
    diseases_len = len(disease_list)

    url_prefix = 'https://www.malacards.org/search/results?query='
    for disease_name in disease_list:
        disease_data = ({"disease": disease_name, "link": "no_match"})
        urlpage = url_prefix + disease_name
        #print(urlpage)
        driver.get(urlpage)
        time.sleep(3)
        match_quality = 0.0
        try:
            match_quality = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/table/tbody/tr[2]/td[7]").text
        except NoSuchElementException:  # spelling error making this code not work as expected
            pass
        disease_result_name = "no_match"
        if (float(match_quality)) > 1.75:
            result = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/table/tbody/tr[2]/td[5]")
            disease_result_name = result.text
            link = result.find_element_by_tag_name('a')
            disease_link = link.get_attribute("href")
            # append dict to array
            disease_data = ({"disease name": disease_name, "disease name result": disease_result_name, "link": disease_link})
        disease_result_list.append(disease_data)
        progress += 1
        print("[" + str(progress) +"/" + str(diseases_len) + "]" + "result" + disease_result_name)
    driver.quit()
    return disease_result_list
    #return disease_data
    #
    #    print(soup)
    # print("bla")
'''