
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome(ChromeDriverManager().install())


import threading

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By


def checkIndex():
    index = input('Enter the index: ')
    while True:
        input1 = driver.find_element(By.CLASS_NAME, 'form-control')
        input1.send_keys(index)
        button = driver.find_element(By.CLASS_NAME, 'btn')
        button.click()
        driver.implicitly_wait(5)
        try:
            text = driver.find_element(By.TAG_NAME, 'table')
            tbody = driver.find_element(By.TAG_NAME, 'tbody')
            icons = tbody.find_elements(By.TAG_NAME, 'td')
            l = []
            for icon in range(len(icons)):
                try:
                    icons[icon].find_element(By.CLASS_NAME, 'glyphicon-ok')
                except NoSuchElementException:
                    l.append(False)
                else:
                    l.append(True)
            print('There is a possibility of delivery by this index')
            print(
                f'LUN - {"Yes" if l[0] else "No"}, MAR - {"Yes" if l[1] else "No"}, MIE - {"Yes" if l[2] else "No"},'
                f' JUE - {"Yes" if l[3] else "No"}, VIE - {"Yes" if l[4] else "No"}, SAB - {"Yes" if l[5] else "No"}')
        except NoSuchElementException:
            print('There is no delivery to this index')
        index = input('Enter the index: ')


options = ChromeOptions()
options.headless = True
driver = webdriver.Chrome("/Users/simmetria0/Desktop/parser/chromedriver.exe",options=options) 

#driver = webdriver.Chrome(options=options)
driver.get('http://zonaextendida.com/')
thread = threading.Thread(target=checkIndex())
thread.start()
