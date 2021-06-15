import pandas as pd
from ej1 import *

'''
Comentario Ejercicio 2
El hecho de escoger únicamente las columnas concretas y
eliminar desde la lectura los registros nulos hace que el número total de valores disminuya
aumentando la eficiencia del método.

Cabe destacar que se han quitado los registros nulos pero solamente de las columnas que realmente se usan a lo largo del ejercicio.
Es decir, no estamos eliminando filas de más ya que los registros nulos tendrían que ser eliminados en algún punto del ejercicio.
Con lo que, para unificar el dataframe, se quitan al crearlos.
'''

def get_clean_data_xlsx(xlsx_filename,cols):
    ''' Este método se encargará de recoger los datos de cualquier xlsx y limpiarlos bajo el mismo estandar:
    quitar los elementos nulos, los strings en minuscula y sustituir los espacios por barra baja'''
    raw_data=pd.read_excel(xlsx_filename,usecols=cols,na_filter=True,keep_default_na=False,engine='openpyxl')
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


def get_raw_main_data():
    '''
    Desde este método se llama aquellos que leen y limpian archivos de formato csv o xlsx.
    El resultado de esta función es una tupla de 3 pandas dataframes con todos los datos necesarios
    para hacer los análisis posteriores.
    '''
    fields_approval_poll=['pollster','tracking','text','party','subject','approve',
    'disapprove','sample_size']
    fields_concern_polls=['pollster','tracking','text','party','subject',
    'not_at_all','very','not_very','somewhat','not_at_all','sample_size','end_date']
    fields_pollster_ratings=['Pollster','Banned by 538','538 Grade','Predictive    Plus-Minus',
    '# of Polls']
    
    raw_approval_poll=get_clean_data_csv('./data/covid_approval_polls.csv',fields_approval_poll)
    raw_concern_poll=get_clean_data_csv('./data/covid_concern_polls.csv',fields_concern_polls)
    raw_pollster_ratings=get_clean_data_xlsx('./data/pollster_ratings.xlsx',fields_pollster_ratings)
    
    return raw_approval_poll,raw_concern_poll,raw_pollster_ratings

def check_pollster(pollster_name,pollster_ratings_data):
    '''
    Debido a que hay varios checks sobre el agente entrevistador y puede haber más.
    Se crea esta función para que sea más sencilla la adición de más capas de condiciones.
    El objetivo es no hacer un loop por filtro sino que en un solo loop de la polls tengamos
    todos los filtros sobre los pollsters.
    '''
    
    # Primera condicion. El agente entrevistador está en la tabla de ratings
    bool_pollster_rated=pollster_name in pollster_ratings_data['Pollster'].values
    
    # Tercera condicion. Agentes no baneados
    bool_pollster_banned=pollster_ratings_data[pollster_ratings_data['Pollster']==pollster_name]['Banned by 538'].values=='no'
    
    bool_pollster=(bool_pollster_rated and bool_pollster_banned[0])
    
    return bool_pollster
    
def main_build_main_data():
    '''
    Este método filtra con las condiciones interpuestas a los datos en bruto de las diferentes fuentes.
    '''
    raw_main_data=get_raw_main_data()
    raw_approval_poll,raw_concern_poll,raw_pollster_ratings=raw_main_data[0],raw_main_data[1],raw_main_data[2]
    
    approval_polls=raw_approval_poll[[
                                    (check_pollster(poll['pollster'],raw_pollster_ratings)
                                    and str(poll['tracking']).lower()=="false")
                                    for index,poll in raw_approval_poll.iterrows()
                                    ]].reset_index()
    
    concern_polls=raw_concern_poll[[
                                    (check_pollster(poll['pollster'],raw_pollster_ratings)
                                    and str(poll['tracking']).lower()=="false")
                                    for index,poll in raw_concern_poll.iterrows()
                                    ]].reset_index()
    
    main_data={'approval_polls':approval_polls,
                'concern_polls':concern_polls,
                    'pollster_ratings':raw_pollster_ratings}
    
    return main_data
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    