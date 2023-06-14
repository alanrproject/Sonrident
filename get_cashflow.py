import pandas as pd

def get_cashflow(df1, df2):
         
    dict_cf = ['Resultado Bruto en ventas','Resultado neto en operaciones',
               'Resultado antes de impuestos','Impuesto a la renta','Resultado neto']

    dff = pd.concat([df1,df2], ignore_index=True, axis=0)
    dff = dff.loc[:,['fecha','valor','FC','AccountID']]
    dff = dff.loc[(dff['AccountID'] > 0),:]

    for x in dict_cf:
        if x == 'Resultado Bruto en ventas':
            d = pd.DataFrame(dff.groupby(['fecha']).sum()['valor'])
            d = d.reset_index()
            d['FC'] = x
            d['AccountID'] = 6
            dff = pd.concat([dff,d], ignore_index=True, axis=0)
        elif x == 'Resultado neto en operaciones':
            d = dff.loc[~(dff['AccountID'] < 6),:]
            d = d.groupby(['fecha']).sum()['valor']
            d = d.reset_index()
            d['FC'] = x
            d['AccountID'] = 10
            dff = pd.concat([dff,d], ignore_index=True, axis=0)
        elif x == 'Resultado antes de impuestos':
            d = dff.loc[~(dff['AccountID'] < 10),:]
            d = d.groupby(['fecha']).sum()['valor']
            d = d.reset_index()
            d['FC'] = x
            d['AccountID'] = 13
            dff = pd.concat([dff,d], ignore_index=True, axis=0)
        elif x == 'Impuesto a la renta':    
            d = dff.loc[(dff['AccountID'] == 13),:]
            d = d.reset_index()
            d['valor'] *= -0.3
            d['AccountID'] = 14
            dff = pd.concat([dff,d], ignore_index=True, axis=0)
        elif x == 'Resultado neto':
            d = dff.loc[~(dff['AccountID'] < 13),:]
            d = d.groupby(['fecha']).sum()['valor']
            d = d.reset_index()
            d['FC'] = x
            d['AccountID'] = 15
            dff = pd.concat([dff,d], ignore_index=True, axis=0)
       
    return dff