from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains



zillow = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(zillow)


page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")


data = soup.find_all(class_='list-card list-card-additional-attribution list-card_not-saved')
property_list = []
for point in data:
    try:
        address = point.find(class_='list-card-addr').get_text()
        price = point.find(class_='list-card-price').get_text().strip('/mo')
        link = point.find('a', href=True)['href']
        prop_dict = {
            "address": address,
            "price": price,
            "link": link
            }
        property_list.append(prop_dict)
    except:
        pass
driver.close()

form = "https://docs.google.com/forms/d/e/1FAIpQLSfys2v7qnXDY9YMNUs9NFohI1ZKjVi28yftEXTLxhfLt_7BIw/viewform"
driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver2.get(form)
for i in property_list:

    time.sleep(1)
    addr = driver2.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    addr.send_keys(i["address"])
    time.sleep(1)
    pric = driver2.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    pric.send_keys(i["price"])
    time.sleep(1)
    lnk = driver2.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    lnk.send_keys(i["link"])
    time.sleep(1)
    bttn = driver2.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    bttn.click()
    time.sleep(1)
    bak = driver2.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    bak.click()

driver2.close()


