from ej1 import *
from ej2 import *
from ej3 import *
from ej4 import *

import pandas as pd
import numpy as np
from datetime import datetime as dt

'''
Comentario Ejercicio 5

Podemos apreciar la misma tendencia en ambas gráficas, tanto con valores absolutos como porcentuales, y es que parece que el número de aquellos que están "very concern" crece. Pero la variación es mínima. Está claro que ya había mucha gente preocupada en septiembre del año pasado, y esa concienciación continúa.
'''

def main_plot_grades_analysis():
    '''
    Este método es el que llama las diferentes funciones para responder al análisis.
    Se trabaja con los datos de las entrevistas sobre la concienciación ciudadana frente los efectos de la pandemia.
    
    En este método se define el valor de la fecha divisoria.
    También se selecciona la nota de corte para los agentes entrevistadores.
    '''
    main_data=main_build_main_data()
    concern_polls=main_data['concern_polls']
    pollster_ratings=main_data['pollster_ratings']
    polls_grade_mapped=build_polls_grade_mapped(pollster_ratings)
    
    polls_grade_credibility=build_polls_grade_credibility(polls_grade_mapped)
    
    date_filter_value='2020-09-01'
    grade_filter_value=1.5
    
    people_distr_date_poll_abs=build_people_distr_date_poll(concern_polls,polls_grade_credibility,date_filter_value,grade_filter_value,'absolute')
    people_distr_date_poll_perc=build_people_distr_date_poll(concern_polls,polls_grade_credibility,date_filter_value,grade_filter_value,'percentage')
    
    do_plot_grades_dates_analysis(people_distr_date_poll_abs,date_filter_value,'people_distr_date_poll_abs.png')
    do_plot_grades_dates_analysis(people_distr_date_poll_perc,date_filter_value,'people_distr_date_poll_perc.png')
    
def build_polls_grade_credibility(data):
    '''
    Este método calcula y añade el credibility sobre el dataframe de origen.
    Este campo es una métrica que nos ayuda a valorar la calidad del agente encuestador y filtrar sus entrevistas.
    Input:
        - Dataframe con datos de las notas por agente entrevistados y Predictive Plus-Minus
    Output:
        - Mismo Dataframe con un campo llamado "credibility" que se calcula como la suma de la nota y el Predictive Plus-Minus
    '''
    grade_map={'a':1,'b':0.5,'c':0,'d':-0.5,'f':-1}
    polls_grade_credibility=data.copy()
    
    data['grade_marks']=data.replace({'grade_reclass':grade_map})['grade_reclass']
    data['credibility']=data['grade_marks']+data['Predictive    Plus-Minus']
    
    polls_grade_credibility['credibility']=data['credibility']
    
    return polls_grade_credibility

def build_people_distr_date_poll(concern_data,polls_data,raw_date,grade_filter,unit):
    '''
    Este método genera un dataframe facilmente explotable en el que se indica el número de personas antes y después por nivel de concienciación.
    Input:
        - Dataframe de los datos de las entrevistas sobre la concienciación.
        - Dataframe de los datos de los agentes entrevistadores.
        - Fecha límite que separa las entrevistas.
        - Nota por la cual filtrar los agentes.
        - Unidad que emplear para los datos: valores absolutos o valores porcentuales.
    Output:
        - Dataframe con tres campos:
            - Un campo para los valores anteriores del número de personas.
            - Un campo para los valores posteriores del número de personas.
            - Un campo que clasifica el nivel de concienciación.
    '''
    concern_fields=['very','not_very','somewhat','not_at_all']
    concern_data_filtr_grade=build_concern_polls_grade_filter(grade_filter,concern_data,polls_data)
    
    concern_data_before,concern_data_after=build_concern_polls_date_filter(
                                                raw_date,concern_data_filtr_grade)
    
    people_distr_date_poll_dict=build_people_distr_date_poll_dict(concern_data_before,concern_data_after,concern_fields,unit)
    
    people_distr_date_poll=pd.DataFrame({'before':list(people_distr_date_poll_dict['people_distr_date_poll_before'].values()),
                                        'after':list(people_distr_date_poll_dict['people_distr_date_poll_after'].values()),
                                        'concern':concern_fields})
    
    return people_distr_date_poll

    
    
    
def build_concern_polls_grade_filter(grade_filter,concern_data,polls_data):
    '''
    Este método filtra las entrevistas por la credibilidad del agente entrevistador.
    Input:
        - Dataframe de los datos de los agentes entrevistadores.
        - Dataframe de las entrevistas sobre concienciación.
        - Valor de la credibilidad por el cual filtrar a los agentes.
    Output:
        - Mismo dataframe de entrada sin los registros que no pasan el filtro.
    '''
    pollster_filtered=polls_data[polls_data['credibility']>=grade_filter]['Pollster'].values
    concern_data_filtr_grade=concern_data[[ 
                                        p in pollster_filtered 
                                            for p in concern_data['pollster']
                                        ]]
    return concern_data_filtr_grade

def build_concern_polls_date_filter(raw_date,concern_data):
    '''
    Este método divide un dataframe por la fecha de finalización de las entrevistas.
    
    Input:
        - Fecha con formato AÑO-MES-DIA, por ejemplo: "2021-01-20"
        - Dataframe con los datos de las entrevistas, asegurándose que contiene la fecha de finalización.
    
    Output:
        - Una tupla de dos dataframes.
            - El primero será el de las entrevistas que terminaron antes de la fecha filtro.
            - El segundo será el de las entrevistas que terminaron después de la fecha filtro.
    '''
    try:
        dt_date=dt.strptime(raw_date,'%Y-%m-%d')
    except Exception as e:
        print(e)
        print('La fecha ha de estar en el siguiente formato: año-mes-dia, por ejemplo: 2020-09-21')
        return 0
    
    concern_data_before=concern_data[[
                                        dt.strptime(d,'%Y-%m-%d')<=dt_date
                                        for d in concern_data['end_date']
                                     ]]
    
    concern_data_after=concern_data[[
                                        dt.strptime(d,'%Y-%m-%d')>=dt_date
                                        for d in concern_data['end_date']
                                     ]]
    return concern_data_before, concern_data_after

def build_people_distr_date_poll_dict(concern_data_before,concern_data_after,concern_fields,unit):
    '''
    Este método calcula los valores de gente según su nivel de concienciación antes y después de una fecha dando como resultado una diccionario.
    Input:
        - Dataframe de los datos de las entrevistas antes de una fecha.
        - Dataframe de los datos de las entrevistas después de una fecha.
        - Campos del nivel de concienciación que se quieren emplear.
        - Unidad en la que estará el resultado: valor absoluto (absolute) o porcentaje (porcentage)
    
    Output:
        - Un diccionario que contiene dos diccionarios de valores:
            - El primer diccionario es el de los valores antes de la fecha seleccionada.
                Su nombre: "people_distr_date_poll_before"
            - El segundo diccionario es el de los valores después de la fecha seleccionada.
                Su nombre: "people_distr_date_poll_after"
            
            Dentro de cada diccionario habrá una pareja clave-valor con este formato:
                "nivel de concienciación":valor numérico
            Por ejemplo:
                "very":15
    '''
    t_field='sample_size'
    unit=unit.lower()
    people_distr_date_poll_before,people_distr_date_poll_after={},{}
    
    if unit=='absolute':
        concern_data_before=build_absolute_numbers_data(concern_fields,
            t_field,concern_data_before)
        
        concern_data_after=build_absolute_numbers_data(concern_fields,
            t_field,concern_data_after)
        
        for c in concern_fields:
            people_distr_date_poll_before[c]=sum(concern_data_before[c].replace('',0).astype(float))
            people_distr_date_poll_after[c]=sum(concern_data_after[c].replace('',0).astype(float))
        
    elif unit=='percentage':
        for c in concern_fields:
            people_distr_date_poll_before[c]=np.mean(concern_data_before[c].replace('',0).astype(float))
            people_distr_date_poll_after[c]=np.mean(concern_data_after[c].replace('',0).astype(float))
            
    elif unit!='percentage':
        print('La unidad escogida no es correcta. \
            Los valores permitidos son "absolute" y "percentage"')
        return 0
    
    
    people_distr_date_poll_dict={
                                    'people_distr_date_poll_before':people_distr_date_poll_before,
                                    'people_distr_date_poll_after':people_distr_date_poll_after
                                }
    
    return people_distr_date_poll_dict  



def do_plot_grades_dates_analysis(distr_data,date_value,pic_name):
    '''
    Este método crea y guarda una gráfica sobre el número de personas y su concienciación, antes y despues.
    Input:
        - Dataframe sobre la distribución del número de personas.
        - Fecha divisoria para personalizar el título del gráfico.
        - Nombre de la imagen del gráfico.
    '''
    classes_name=distr_data['concern'].values
    indexes_bar = np.arange(len(classes_name)*2+1)
    before_data,after_data=distr_data['before'].values,distr_data['after'].values
    wid=1
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    
    ax.bar(color='khaki',height=before_data,x=indexes_bar[:len(classes_name)],width=wid)
    ax.bar(color='white',height=before_data[0],x=indexes_bar[len(classes_name)],width=wid)
    ax.bar(color='coral',height=after_data,x=indexes_bar[len(classes_name)+1:],width=wid)
    ax.set_xticks(indexes_bar)
    ax.set_xticklabels(list(classes_name)+list([''])+list(classes_name))
    
    plt.legend(['Before','','After'])
    plt.title(f'Distribución de la concienciación de las personas antes y después de {date_value}')
    plt.savefig(pic_name)
    
    plt.close()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    