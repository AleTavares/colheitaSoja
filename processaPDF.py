# Para processar arquivos PDF
from PyPDF2 import PdfFileReader
import coletaLinkPDFSoja as pdfSoja
import requests
import io
import pandas as pd
from tabula import read_pdf
def processaPDF():
    pdfurls = pdfSoja.scrapingPDF()
    tabelaComum = read_pdf(pdfurls[0])
    print(pdfurls[1])
    # print(tabelaComum[0])
    # variables = tabelaComum[0].keys()
    # dfSoja = pd.DataFrame(tabelaComum, columns = variables)
    dfSoja = pd.DataFrame(tabelaComum[0])
    dfSoja = dfSoja.apply(lambda x: x.head(-6)).reset_index(0, drop=True) 
    dfSoja.pop('Unnamed: 0')
    print(dfSoja)

processaPDF()
