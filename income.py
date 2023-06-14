import pandas as pd

def read_sheet(path, hoja, skr, cols,names):
    df = pd.read_excel(path, sheet_name=hoja, skiprows=skr, usecols=cols,
                    names=names)
    return df

def get_income(dicm,year,dir):
          
    dicd = list(range(1,32))
    df = pd.DataFrame()
    for m in dicm:
        for x in dicd:
            dfaux = pd.DataFrame(read_sheet(dir + m + ' ' + year + '.xlsx','DIA ' + str(x),0,
                    [0,1,2,3,4,5,6],['nombre_paciente','descripción','abono', 'deduccion', 'valo_postdeduccion',
                    'per_sonrident','per_odontologo']))

            ## Borrar datos con nombre de paciente nulo y abono cero:
            dfaux = dfaux.loc[~((dfaux['nombre_paciente'].isnull()) & (dfaux['abono']== 0)),:]
            dfaux['nombre_paciente'] = dfaux['nombre_paciente'].astype('string')
            dfaux.reset_index(drop=True,inplace=True)
            # Crear columna fecha como str y concatenar df
            dfaux['fecha'] = str(x) + '-' + m + '-' + year
            dic = ['abono','deduccion','valo_postdeduccion',
                   'per_sonrident','per_odontologo']
            for j in dic:
                dfn = dfaux[['nombre_paciente','fecha','descripción',j]]
                dfn['FC'] = j
                dfn.rename(columns = {j:'valor'}, inplace=True )
                df = pd.concat([df,dfn], ignore_index=True, axis=0)
    return df