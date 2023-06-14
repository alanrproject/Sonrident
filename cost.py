import pandas as pd
from income import read_sheet


def get_cost(dicm,year,dir):
    dicd = list(range(1,32))
    dfc = pd.DataFrame()
    for m in dicm:
        for x in dicd:
            dfaux = pd.DataFrame(read_sheet(dir + m + ' ' + year +
                     '.xlsx','DIA ' + str(x),0,
                    [8,9],['descripcion_costo','valor']))

            ## Borrar datos con descripción y valor nulo:
            dfaux = dfaux.loc[~((dfaux['descripcion_costo'].isnull()) & (dfaux['valor']== 0)),:]
            dfaux = dfaux.loc[~(dfaux['valor'].isnull()),:]
            dfaux.reset_index(drop=True,inplace=True)
            # Crear columna fecha como str y concatenar df
            dfaux['fecha'] = str(x) + '-' + m + '-' + year
            dfaux['FC'] = 'compra_insumos'
            dfc = pd.concat([dfc,dfaux], ignore_index=True, axis=0)
    return dfc
    