from PyPDF2 import PdfFileReader
import pandas as pd
from tabula import read_pdf
import re
import os
import bancoDados as bd

# Função para limpar sujeira coluna Nordeste
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
# Função para ajustar as datas
def ajustaData(strData):
    mes = {
        'jan': '1',
        'fev': '2',
        'mar': '3',
        'abr': '4',
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

# Função para processar arquivos PDF
def processaPDF():
    # Lê PDF com hitorico de colheita
    tabelaComum = read_pdf('colheita18_19.pdf')
    
    # Tranforma os dados gerados do PDF em um DataFrame
    dfSoja = pd.DataFrame(tabelaComum[0])
    
    # apaga as linhas com sujeira
    dfSoja = dfSoja.dropna()

    # Retira Caracter % e troca virgula por ponto
    for coluna in dfSoja.columns:
        dfSoja[coluna] = dfSoja[coluna].apply(lambda x : str(x).replace("%", ""))
        dfSoja[coluna] = dfSoja[coluna].apply(lambda x : str(x).replace(",", "."))

    # separa colunas que vieram unidas
    new = dfSoja["Norte Oeste"].str.split(" ", n = 1, expand = True)
    dfSoja['Norte'] = new[0]
    dfSoja['Oeste'] = new[1]
    dfSoja.pop('Norte Oeste')

    # Apaga as 2 ultimalinhas geradas para limpar o dataframe
    dfSoja = dfSoja.apply(lambda x: x.head(-2)).reset_index(0, drop=True) 
    dfSoja = dfSoja.iloc[1:]
    dfSoja['Regiões do IMEA'] = dfSoja['Regiões do IMEA'].apply(ajustaData)

    # Retira coluna gerada com sujeira
    dfSoja['Norte'] = dfSoja['Norte'].map(limpaValores)
    
    # Unpivota dados
    df_unpivoted = dfSoja.melt(id_vars=['Regiões do IMEA', ], var_name='regioesIMEA', value_name='percentual')
    df_unpivoted.columns = ['data',  'regioesIMEA', 'percentual']
    
    #insere dados novos na base
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

processaPDF()
