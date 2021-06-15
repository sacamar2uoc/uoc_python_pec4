from ej1 import *
from ej2 import *
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

'''
Explicación Ejercicio 3
Aquí creamos los métodos necesarios para saber la aprobación a Trump filtrando por diferentes entrevistas.
'''

def build_absolute_numbers_data(p_fields,t_field,raw_data):
    '''
    Este método es capaz de pasar de porcentaje a valores absolutos varios campos.
    Sustituye los valores de cada campo porcentual por su valor absoluto.
    Como input necesita los nombres de los campos porcentuales, el nombre del campo que contiene el valor absoluto del 100%
    y el dataframe donde estan todos estos datos. Su ouput es el mismo dataframe pero cambiado el valor porcentual por el absoluto.
    Hay que tener en cuenta que sobreescribe sobre los campos porcentuales.
    '''
    absolute_numbers_data=raw_data.copy()    
    
    for f in p_fields:
        p_num=raw_data[f].replace('',0).astype(float)
        t_num=raw_data[t_field].replace('',0).astype(float)
        absolute_numbers_data[f]=p_num*t_num/100
    
    return absolute_numbers_data

def build_people_approve_disapprove():
    '''
    Este método da el análisis pedido sobre los partidos políticos y su aprobación a Trump.
    Las entrevistas recogidas son las que mencionan a Trump y el coronavirus.
    El output es un dataframe que agrupa por partido político sumando las personas según su postura.
    '''
    main_data=main_build_main_data()
    approval_polls=main_data['approval_polls']
    
    percentage_fields,total_field=['approve','disapprove'],'sample_size'
    
    approval_polls_absolute=build_absolute_numbers_data(percentage_fields,total_field,approval_polls)
    studied_fields=percentage_fields
    studied_fields.append('party')
    
    people_approve_disapprove=approval_polls_absolute[
                                            [(('trump' in t) and ('coronavirus' in t)) 
                                            for t in approval_polls_absolute['text']]
                                         ][studied_fields].groupby(by='party').sum()
    return people_approve_disapprove
    
def do_plot_people_approve_disapprove():
    '''
    Método que genera el gráfico sobre los datos de aprobación calculados en el método "build_people_approve_disapprove".
    Guarda el gráfico con nombre people_approve_disapprove.png .
    No salta la ventana del gráfico porque se ha priorizado la fluided de la ejecución del código.
    '''
    people_approve_disapprove=build_people_approve_disapprove()
    classes_name=['All','Demócratas','Independientes','Republicanos']
    indexes_bar = np.arange(len(classes_name))
    wid=0.2
    
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    approves_bars=ax.bar(color='royalblue',height=people_approve_disapprove['approve'],x=indexes_bar,width=wid)
    disapproves_bars=ax.bar(color='darkred',height=people_approve_disapprove['disapprove'],x=indexes_bar+wid,width=wid)
    plt.xticks(indexes_bar+wid / 2)
    ax.set_xticklabels(classes_name)
    plt.legend(['Personas que lo aprueban','Personas que NO lo aprueban'])
    plt.title('Distribución por partidos de la aprobación a Trump al inicio de la pandemia')
    plt.savefig('people_approve_disapprove.png')
    plt.close()






