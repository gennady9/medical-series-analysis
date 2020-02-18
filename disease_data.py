import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def get_all_disease_data(disease_table):
    not_found = 0
    data = []
    for disease in disease_table:
        current_data = get_disease_data(disease)
        if current_data == "no match":
            not_found += 1
        else:
            data.append(current_data)
    return data

def get_disease_data(disease_name):
    # page = requests.get("https://www.malacards.org/search/results?query=Echovirus+11")
    # soup = BeautifulSoup(page.content, 'html.parser')
    # specify the url
    disease_data = "no match"
    url_prefix = 'https://www.malacards.org/search/results?query='
    urlpage = url_prefix + disease_name
    print(urlpage)
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(executable_path='D:/dhp/geckodriver')

    # get web page
    driver.get(urlpage)
    # execute script to scroll down the page
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match_quality = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[4]/div/table/tbody/tr[2]/td[7]")
    if (float(match_quality.text)) > 1.75:
        result = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[4]/div/table/tbody/tr[2]/td[5]")
        disease_name = result.text
        link = result.find_element_by_tag_name('a')
        disease_link = link.get_attribute("href")
        # append dict to array
        disease_data = ({"disease": disease_name, "link": disease_link})
        # sleep for 30s
    time.sleep(30)
    driver.quit()
    return disease_data
    #
    #    print(soup)
    # print("bla")
