import pandas as pd
import numpy as np
import datetime as dt
from similarity import get_similarity
from income import get_income
from cost import get_cost
from get_cashflow import get_cashflow

folder = 'G:/.shortcut-targets-by-id/11ELOj-8KP7_bxglOaLuJHs00Y5CzC0ly/FLUJOS 2023/'
year = '2023'

if __name__ == '__main__':
    
    df = get_income(['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO',
            'AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'],year,
            folder)    
    
    # Borrar filas total
    df = df.loc[~(df['nombre_paciente'].str.contains('TOTAL')),:]
    df.reset_index(drop=True,inplace=True)

    # Crear columna con nombre odontologo y borrar filas resumen:
    i = 0
    for value in df['nombre_paciente'].astype(str):
        if value.startswith('DOC '):
            doc = value
            df.at[i,'odontologo'] = doc
        elif value.startswith('DRA '):
            doc = value
            df.at[i,'odontologo'] = doc
        elif value.startswith('DR '):
            doc = value
            df.at[i,'odontologo'] = doc
        else:        
            df.at[i,'odontologo'] = doc
        i += 1

    # Borrar filas DR DRA DOC
    for x in ['DOC ','DRA ','DR ']:
        df = df.loc[~(df['nombre_paciente'].str.startswith(x)),:]

    # Corregir nombre de odontólogos
    df.reset_index(drop=True,inplace=True)
    i = 0
    for value in df['odontologo'].astype(str):
            
            words = value.split()
            words = [word.lower() for word in words]
            words = words[1:]
            words = '_'.join(words)
            df.at[i,'odontologo'] = words
            i += 1
    
    drs = {'aleandra_':'alejandra_','allejandra_':'alejandra_','carolina_':'',
           'resptrepo':'restrepo','carolina':'ana_herrera','bedpya':'bedoya',
           'dedoya':'bedoya','carlos_gomez_':'carlos_','maria_alejandra_':'alejandra_',
           'sar_':'sara_','cñas':'cañas','sara_lucia_':'sara_',
           'sarra_':'sara_','yesenia_':'yessenia_'}
    df['odontologo'] = df['odontologo'].replace(drs, regex=True)

    # limpiar fechas falsas
    for x in ['29-FEBRERO','30-FEBRERO','31-FEBRERO','31-ABRIL','31-JUNIO',
                '31-SEPTIEMBRE','31-NOVIEMBRE']:
        df = df.loc[~(df['fecha'].str.contains(x, na=False)),:]
    
    # Limpiar celdas con nombre vacio y valor 0
    df = df.loc[~(df['nombre_paciente'].isnull()),:]
    df = df.loc[~((df['valor']== 0) | (df['valor'].isnull()) | (df['valor']==' ')),:]
    #df = df.loc[~(df['valor'].isnull()),:]
    df.reset_index(drop=True,inplace=True)
    
    # Convertir fecha de string a fecha
    mapdic = {'ENERO':'jan','FEBRERO':'feb','MARZO':'mar',
            'ABRIL':'apr','MAYO':'may','JUNIO':'jun',
            'JULIO':'jul','AGOSTO':'aug','SEPTIEMBRE':'sep',
            'OCTUBRE':'oct','NOVIEMBRE':'nov','DICIEMBRE':'dec'}
    pd.to_datetime(df['fecha'].replace(mapdic, regex=True))
    
    #Crear columna accountID
    i = 0
    df['AccountID'] = 0
    for value in df['FC']:
        if value == 'abono':
            df.at[i,'AccountID'] = 1
        elif value == 'per_odontologo':
            df.at[i,'AccountID'] = 3
            df['valor'][i] *= -1
        i += 1
    
    #calcular valor acumulado
    df['FC'] = df['FC'].astype(str)
    df['valor'] = pd.to_numeric(df['valor'])
    df['valor_total'] = df.groupby(['FC'])['valor'].cumsum()

    #Obtener registros de costo y gasto
    dfc = get_cost(['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO',
            'AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'],year,
            folder)
    
    dfc = dfc.loc[~(dfc['descripcion_costo'].isnull()),:]
    for x in ['INGRESO BRUTO','GASTOS','INGRESO NETO']:
        dfc = dfc.loc[~(dfc['descripcion_costo'].str.contains(x, na=False)),:]
    dfc.reset_index(drop=True,inplace=True)
    # limpiar fechas falsas
    for x in ['29-FEBRERO','30-FEBRERO','31-FEBRERO','31-ABRIL','31-JUNIO',
                '31-SEPTIEMBRE','31-NOVIEMBRE']:
        dfc = dfc.loc[~(dfc['fecha'].str.contains(x, na=False)),:]
    dfc.reset_index(drop=True,inplace=True)
    pd.to_datetime(dfc['fecha'].replace(mapdic, regex=True))
    dfc['AccountID'] = 4
    dfc['valor'] *= -1

    #Concatenar financials
    dff = get_cashflow(df,dfc)    

    # imprimir archivo
    writer = pd.ExcelWriter('df.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='income')
    dfc.to_excel(writer, sheet_name='cost')
    dff.to_excel(writer, sheet_name='financials')
    writer.close()
    