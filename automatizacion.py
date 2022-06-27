import requests as req
import codecs
import json
import pandas as pd
import datetime
import time
from zipfile import ZipFile
import os

def proceso():
    url = 'https://repositoriodeis.minsal.cl/SistemaAtencionesUrgencia/AtencionesUrgencia2022.zip'
    file = req.get(url, allow_redirects=True)
    open('data.rar', 'wb').write(file.content)
    test_file_name = "data.rar"

    with ZipFile(test_file_name, 'r') as zip:
        zip.printdir()
        zip.extractall() 
    df = pd.read_csv("AtencionesUrgencia2022.csv", sep=";", encoding ='latin1')
    df2 =df[['idestablecimiento', 'nestablecimiento', 'Idcausa', 'glosacausa',
       'TOTAL','semana']]
    df3 = df2.groupby(by=['idestablecimiento', 'nestablecimiento', 'Idcausa', 'glosacausa',
       'semana']).sum()
    df3 = df3.reset_index()
    data = df3[['idestablecimiento', 'Idcausa', 'semana', 'TOTAL']]
    #print(len(data))
    #df2 = df[['IdEstablecimiento', 'NEstablecimiento', 'IdCausa', 'GlosaCausa', 'GLOSATIPOESTABLECIMIENTO', 'GLOSATIPOATENCION','GlosaTipoCampana', 'Año']]
    #df2 = df2.drop_duplicates()
    #df2 = df2[df2["Año"] == i]
    #merge = data.merge(df2,left_on=["IdEstablecimiento","IdCausa"],right_on=["IdEstablecimiento","IdCausa"], how="left")
    #print(len(merge))
    #merge.to_excel(f"data/data_urgencia_{i}.xlsx", index=False)
    data2 = df3[['idestablecimiento', 'nestablecimiento', 'Idcausa', 'glosacausa']]
    data2 = data2.drop_duplicates()
    avance = data2
    for j in data["semana"].unique():
            dfaux =data[data["semana"] == j]
            dfaux[f"Semana {j}"] = dfaux["TOTAL"]
            del dfaux["TOTAL"]
            del dfaux["semana"]
            #dfaux = dfaux.drop_duplicates(subset=["IdEstablecimiento","IdCausa"])
            
            avance = avance.merge(dfaux, left_on=["idestablecimiento","Idcausa"],right_on=["idestablecimiento","Idcausa"], how="left",validate="one_to_one")
            
    del avance["Semana 52"]
    avance.to_excel("avance.xlsx", index=False)
    os.remove("AtencionesUrgencia2022.csv")
    return

if __name__ == '__main__':
    print("Cerradas...")
    