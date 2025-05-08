import pickle
import locale
import pandas as pd
import streamlit as st
import datetime
from datetime import date
from datetime import timedelta
from io import BytesIO
from os import path
import os
import streamlit.components.v1 as components

def countCurUseFul(dateTuple):
    dateIni = dateTuple[0]
    num = dateTuple[1]
    mode = dateTuple[2]
    expr = dateTuple[3]
    dateIniStr = dateIni.strftime("%d/%m/%Y")
    dateIniName = dateIni.strftime("%#d de %B de %Y")
    count = 0 
    n = 0 
    colStart, colDays, colCrit = st.columns(spec=3, gap='small', vertical_alignment='top', border=True)
    colStart.markdown(f'**Data inicial**  : {dateIniStr} ({dateIniName})')
    colDays.markdown(f'**Número de dias**: {num}')
    colCrit.markdown(f"**Critério**: ***:blue-background[{expr}]***")
    while count < num:
        dateNew = dateIni + datetime.timedelta(days=n)
        weekNum = dateNew.weekday()
        weekName = dateNew.strftime("%A")
        dateFormat = dateNew.strftime("%d/%m/%Y")
        dateName = dateNew.strftime("%#d de %B de %Y")
        if n == 0:
            status = 'não conta'
        else: 
            if mode == 0:
                if count == num - 1: 
                    if any ([weekNum == 5 or weekNum == 6]):
                        status = 'não conta'
                    else:
                        status = 'conta'
                        count += 1
                else:
                    status = 'conta'
                    count += 1
            else:
                if any ([weekNum == 5 or weekNum == 6]):
                    status = 'não conta'
                else:
                    status = 'conta'
                    count += 1
        if status == 'conta': 
            countStr = f'{str(count)}.°'
        else: 
            countStr = ''        
        infoCombo = [f'{dateFormat} ({dateName})', weekName, status, countStr, n + 1]
        for i, info in enumerate(infoCombo):
            key = keyCurrent[i]
            dateCurrUse[key].append(info)    
        n += 1

# Function to convert DataFrame to Excel file in memory
def toCsv():
    csv = df.to_csv(index=False).encode('ISO-8859-1')
    return csv

def toPickle():
    pkl = pickle.dumps(df)
    return pkl

def toHtml():
    htmlText = df.to_html(index=False)
    hmtlPlus = """
    <style>
        .button {
          background-color: #04AA6D; /* Green */
          border: None;
          color: white;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 13px;
          margin: 6px 2px;
          cursor: pointer;
        }
        .button1 {padding: 8px 14px;}
    </style>
    <button class="button button1" onclick=window.print()>Imprime</button>
    """    
    htmlText += f"<body>{hmtlPlus}</body>"
    return htmlText
    
def toTxt():
    txt = df.to_string(index=False).encode('ISO-8859-1')
    return txt
 
def toJson():
    json = df.to_json()
    return json
    
def toTex():
    tex = df.to_latex()
    return tex

def toStata(fileDta):
    dta = df.to_stata(fileDta)

def iniVars():
    labels = {'csv':['dfTable.csv', "Download da tabela para o formato 'csv'.", ":material/download:"], 
              'pickle': ['dfTable.pkl', "Download da tabela para o formato 'pickle'.", ":material/download:"], 
              'html': ['dfTable.html', "Download da tabela para o formato 'html'.", ":material/download:"], 
              'txt': ['dfTable.txt', "Download da tabela para o formato 'txt'.", ":material/download:"], 
              'json': ['dfTable.json', "Download da tabela para o formato 'json'.", ":material/download:"], 
              'latex': ['dfTable.tex', "Download da tabela para o formato 'tex'.", ":material/download:"]
             }
    keys = list(labels.keys())
    with st.container(border=False):
        st.markdown(f":point_right: **:blue[opções]**")
        #Csv
        colCsv, colPkl, colHtml = st.columns(spec=3, gap='small', vertical_alignment='center', border=False)
        colString, colJson, colLatex = st.columns(spec=3, gap='small', vertical_alignment='top', border=False)
        colCsv.download_button(
            label=keys[0],
            use_container_width=True, 
            data=toCsv(),
            file_name=labels[keys[0]][0],
            mime='text/csv', 
            help=labels[keys[0]][1], 
            icon=labels[keys[0]][2]
        )
        #Pkl
        colPkl.download_button(
            label=keys[1],
            use_container_width=True, 
            data=toPickle(),
            file_name=labels[keys[1]][0],
            mime="application/octet-stream", 
            help=labels[keys[1]][1], 
            icon=labels[keys[1]][2]
        )   
        #Html
        colHtml.download_button(
            label=keys[2],
            use_container_width=True, 
            data=toHtml(),
            file_name=labels[keys[2]][0], 
            help=labels[keys[2]][1], 
            icon=labels[keys[2]][2]
        )
        #String
        colString.download_button(
            label=keys[3],
            use_container_width=True, 
            data=toTxt(),
            file_name=labels[keys[3]][0], 
            help=labels[keys[3]][1], 
            icon=labels[keys[3]][2]
        )
        #Json
        colJson.download_button(
            label=keys[4],
            use_container_width=True,
            data=toJson(),
            file_name=labels[keys[4]][0], 
            help=labels[keys[4]][1], 
            icon=labels[keys[4]][2]
        )
        #Tex
        colLatex.download_button(
            label=keys[5],
            use_container_width=True,
            data=toTex(),
            file_name=labels[keys[5]][0], 
            help=labels[keys[5]][1], 
            icon=labels[keys[5]][2]
        )
        
def main():
    global output, dirRoot
    global keyCurrent, keyUseFul
    global dateCurrUse, df
    keyCurrent = ['dia do mês', 'dias da semana', 
                  'condição', 'sequencial', 'contador geral']
    dateCurrUse = {key:[] for key in keyCurrent}
    dateNow = datetime.date.today()
    d = date(2025, 5, 9)
    #args = [(d, 12, 0, 'Contagem em dias corridos', 'Demonstrativo 1'), 
    #        (d, 12, 1, 'Contagem em dias úteis', 'Demonstrativo 2')]
    #Somente dias corridos
    args =  [(d, 12, 1, 'Contagem em dias úteis', 'demonstrativo único')]
    for a, arg in enumerate(args):
        #st.divider()
        if a == (len(args) - 1): 
            st.write('')
            st.write('')
        st.markdown(f":page_with_curl: **:blue[{arg[-1]}]**")
        countCurUseFul(arg)
        df = pd.DataFrame(dateCurrUse)
        st.dataframe(data=df, hide_index=True, use_container_width=True)
        output = BytesIO() 
        dateCurrUse.clear()
        dateCurrUse = {key:[] for key in keyCurrent}
    iniVars()    

if __name__ == '__main__':
    st.markdown("# Cálculo de dias úteis 📙")
    main()