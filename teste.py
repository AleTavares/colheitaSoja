from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
# driver = webdriver.Chrome("chromedriver.exe")
option = Options()
option.headless = True
driver = webdriver.Chrome()

driver.get("http://www.imea.com.br/imea-site/relatorios-mercado-detalhe?c=4&s=8")
time.sleep(1) # Aguarde o carregamento dos dados
td_valor_list = driver.find_elements_by_class_name("list-link")
print(td_valor_list)