from PyPDF2 import PdfFileReader
import coletaLinkPDFSoja as pdfSoja
import pandas as pd
from tabula import read_pdf
import re
import bancoDados as bd

#função para limpar sujeira coluna Nordeste
def limpaValores(strLimpar):
    if "/" in strLimpar:
        arrTemp = strLimpar.split('/')
        formulaRegex = r"\D"
        valorPosVirgula = re.sub(formulaRegex, "", arrTemp[1])
        ValorAntesVirgula = str(arrTemp[0][len(arrTemp[0])-3])+str(arrTemp[0][-1])
        retorno = str(ValorAntesVirgula) + '.' + str(valorPosVirgula)
    else:
        retorno = strLimpar
    return retorno
def ajustaData(strData):
    mes = {
        'jan': '1',
        'fev': '2',
        'mar': '3',
        'abr': '4',
        'mai': '5',
        'jun': '6',
        'jul': '7',
        'ago': '8',
        'set': '9',
        'out': '10',
        'nov': '11',
        'dez': '12'
    }
    arrData = strData.split('-')
    dataAjustada = '20'+arrData[2] + '-' + mes[arrData[1]] + '-' + arrData[0]
    return dataAjustada

# Funcção para processar arquivos PDF
def processaPDF():
    pdfurls = pdfSoja.scrapingPDF()
    # Pega a primeira linha do Dataframe, pois o ultimo publicado acumula os dados
    tabelaComum = read_pdf(pdfurls[0])

    # Tranforma os dados gerados do PDF em um DataFrame
    dfSoja = pd.DataFrame(tabelaComum[0])
    dfSoja.pop('Unnamed: 0')
    for coluna in dfSoja.columns:
        dfSoja[coluna] = dfSoja[coluna].apply(lambda x : str(x).replace("%", ""))
        dfSoja[coluna] = dfSoja[coluna].apply(lambda x : str(x).replace(",", "."))
    dfSoja['Regiões do IMEA Centro-Sul'] = dfSoja['Regiões do IMEA Centro-Sul'].apply(lambda x : str(x).replace("10/jan", ""))
    
    new = dfSoja["Regiões do IMEA Centro-Sul"].str.split(" ", n = 1, expand = True)
    dfSoja['data'] = new[0]
    dfSoja['Centro-Sul'] = new[1]
    dfSoja.pop('Regiões do IMEA Centro-Sul')
    
    # Apaga as 6 ultimalinhas geradas para limpar o dataframe
    dfSoja = dfSoja.apply(lambda x: x.head(-6)).reset_index(0, drop=True) 
    dfSoja['data'] = dfSoja['data'].apply(ajustaData)
    
    # Retira coluna gerada com sujeira
    dfSoja['Nordeste'] = dfSoja['Nordeste'].map(limpaValores)
    
    df_unpivoted = dfSoja.melt(id_vars=['data', ], var_name='regioesIMEA', value_name='percentual')
    sql = "insert into soja.producaoSoja(\
                    datacotacao, \
                    regioesimea, \
                    percentual\
                ) values"
    conectaInsert = ''
    executa = False
    for index, row in df_unpivoted.iterrows():
        bd.cur.execute("select datacotacao\
                        from soja.producaosoja \
                        where datacotacao = '" + row['data'] + "' \
                        and regioesimea = '" + row['regioesIMEA'] + "'")
        recset = bd.cur.fetchall()
        if len(recset) <= 0:
            sql = sql + conectaInsert + "(\
                            '" + row['data'] +"',\
                            '" + row['regioesIMEA'] +"',\
                            " + row['percentual'] +"\
                        )"
            executa = True
            conectaInsert = ', '
    if executa:
        bd.cur.execute(sql)
        bd.con.commit()
    bd.con.close()
    print(df_unpivoted)
