import pandas as pd
import re
import dask.dataframe as dd

    
'''
Comentario Ejercicio 2

1.2 ¿Si tuviéramos un archivo de 1Gb lo harías igual? Si no es así, implementar la solución para este caso.
Al ser un único archivo tan grande usaría librería optimizadas para ello como Dask. En mi experiencia es la más familiar cuando se tiene experiencia con pandas. La implementación está en la función get_clean_data_big.

1.3 ¿Si tuviéramos 100 archivos de 1Gb cómo lo harías? No hace falta implementar la solución, sólo una pequeña descripción de cómo resolverías el problema.
La función implementada en la sección 1.2 del ejercicio sería llamada en concurrencia usando multithreading.
Se haría una lista de los nombres de cada csv y se pasaría a la función que tuviera el multithread, su ouput sería fusionado en un dataframe de dask o un parquet.
'''

def main_do_message_covid_approval_polls():
    '''
    Muestra los datos de la frecuencia de los patrones por pantalla.
    '''
    freq_patterns=build_freq_patterns_covid_approval_polls()
    print(f'There are {freq_patterns[0]} polls sponsored by Huffington Post')
    print(f'There are {freq_patterns[1]} polls showing its info on pdf format')


def get_clean_data_csv(csv_filename,cols="all"):
    ''' Este método se encargará de recoger los datos de cualquier csv y limpiarlos bajo el mismo estandar:
    quitar los elementos nulos, los strings en minuscula y sustituir los espacios por barra baja'''
    if cols=="all":
        raw_data=pd.read_csv(csv_filename,na_filter=True,keep_default_na=False)
    else:
        raw_data=pd.read_csv(csv_filename,usecols=cols,na_filter=True,keep_default_na=False)
    col_names=raw_data.columns.values
    clean_data=pd.DataFrame()
    
    for cn in col_names:
        aux_field=raw_data[cn]
        try:
            clean_data[cn]=[aux_row.lower().replace(" ","_") for aux_row in raw_data[cn]]
        except Exception as e:
            clean_data[cn]=raw_data[cn]
            pass
    
    return clean_data

def build_freq_patterns_covid_approval_polls():
    '''
    Este método calcula la frecuencia de dos patrones en los campos sponsor y url.
    Su output es una tupla de dos valores float.
    '''
    hp_pattern="huffington_post"
    http_pattern=r"http:\/\/(.*)[.]pdf|https:\/\/(.*)[.]pdf"
    freq_hp,freq_http=0,0
    
    field_names=['sponsor','url']
    
    try:
        covid_approval_polls=get_clean_data_csv("./data/covid_approval_polls.csv",field_names)
    except Exception as e:
        print(e)
        return 1
    
    for i in range(len(covid_approval_polls)):
        aux_sponsors=covid_approval_polls['sponsor'].iloc[i]
        aux_url=covid_approval_polls['url'].iloc[i]
        freq_http+=1 if (len(re.findall(http_pattern,aux_url))>0) else 0
        freq_hp+=1 if aux_sponsors==hp_pattern else 0
    return freq_http,freq_hp


def get_clean_data_big(csv_filename):
    '''
    Este método esta especialmente diseñado para leer archivos de gran tamaño usando la librería dask
    '''
    raw_data=dd.read_csv(csv_filename)
    return raw_data


