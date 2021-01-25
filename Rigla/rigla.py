import requests
import json
import os
from pathlib import Path

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import geckodriver_autoinstaller

from webdriverdownloader import GeckoDriverDownloader

url= 'https://www.rigla.ru/pharmacies'

def get_data(url=None):
    if url is None:
        return False

    header = {'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    driver_path = Path.cwd().parent / '..' / 'geckodriver.exe'

    firefox_profile = webdriver.FirefoxProfile()
    print("wbd")
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    driver = webdriver.Firefox(executable_path=driver_path,
                            firefox_profile=firefox_profile)
    driver.get('https://small.kz/')

#    wd = webdriver.Firefox()
#    wd.get(url)
#    ids = wd.execute_script("return sessionStorage.getItem('pvzCities')")
#    print(ids)

    #s = requests.Session()
    #r = requests.get(url, headers=header)

    #print("-GET-")
    #print(r.text)
    #output = open("rigla.txt", 'w')
    #output.write(r.text)
    #output.close()

    return True

def main ():
    data = get_data(url)

if __name__ == '__main__':
    main()