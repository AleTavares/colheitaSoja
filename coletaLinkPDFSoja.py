import bs4
from bs4 import BeautifulSoup
import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# driver = webdriver.Chrome("chromedriver.exe")
def scrapingPDF():
    # URL com os dados das colheitas de Soja
    url = 'http://www.imea.com.br/imea-site/relatorios-mercado-detalhe?c=4&s=8'

    option = Options()
    option.headless = True
    driver = webdriver.Chrome()
    # Obtém os dados da URL
    driver.get(url)
    time.sleep(1) # Aguarde o carregamento dos dados
    listaLinks = driver.find_element_by_xpath("//div[@id='RelatorioDetalheApp']//section[@class='content']//div[@id='tab-box']//div[@class='col-md-12 tab-body']//div[@class='col-md-8 col-lg-8']")
    response = listaLinks.get_attribute('outerHTML')
    soup = BeautifulSoup(response, 'html.parser')
    # Lista temporária
    pdfurls = []

    # Loop pelos elementos da página para buscar as tags "a" que indicam URLs
    for element in soup.find_all('a', href = True):
        txt = BeautifulSoup(str(element), 'html.parser').a
        pdfurls.append(txt['href'])
    return pdfurls