import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException

gecko_path = "D:/dhp/geckodriver.exe"

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


def get_malacard_data(urlpage):

    disease_data = "no match"
    #url_prefix = 'https://www.malacards.org/search/results?query='
    #urlpage = url_prefix + disease_name
    print(urlpage)
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(executable_path=gecko_path)

    # get web page
    driver.get(urlpage)
    time.sleep(3)
    html = driver.page_source
    driver.quit()

    print(html)

    #return disease_data



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
'''