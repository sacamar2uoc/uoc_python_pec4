from ej1 import *
from ej2 import *
from ej3 import *

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable


'''
4. Sobre los datos extraídos en el ejercicio 2 de la tabla concern_polls, teniendo en cuenta las
siguientes transformaciones sobre el grado en la clasificación (grade) *, calculad y representad
gráficamente (excepto el 4.1):
4.1 Cuánta gente ha participado en las entrevistas. Representar el resultado por pantalla
debidamente formatado.
4.2 Cuánta gente en la materia (subject) de la entrevista relacionada con la economia (economy)
está very (concern, preocupación) y cuánta está not_at_all (concern, preocupación).
4.3 Cuál es el porcentaje de gente en la matèria (subject) de la entrevista relacionada con la
infección (
'''

def main_concern_polls_analysis():
    '''
    Este método llama a todas las funciones que dan un análisis de los resultados de las entrevistas sobre la concienciación.
    Estas entrevistas evalúan la concienciación ciudadana sobre la pandemia y sus efectos.
    '''
    main_data=main_build_main_data()
    concern_polls=main_data['concern_polls']
    pollster_ratings=main_data['pollster_ratings']
    
    poll_participation=sum(concern_polls['sample_size'])
    
    print(f'En las entrevistas para la concienciación sobre el impacto \
    del coronavirus en tu entorno cercano \
    han participado {int(poll_participation)} personas.')
    
    people_economy_concern=build_people_distr_concern('economy',concern_polls,'absolute')
    do_plot_concerns(people_economy_concern,'people_economy_concern.png','economy')
    
    people_infected_concern=build_people_distr_concern('infected',concern_polls,'percentage')
    do_plot_concerns(people_infected_concern,'people_infected_concern.png','infected')
    
    poll_per_grade=build_poll_per_grade(pollster_ratings)
    do_plot_polls_grade(poll_per_grade,'poll_per_grade.png')

    
def build_people_distr_concern(topic,data,unit):
    '''
    Método para calcular la distribución de las personas por su nivel de preocupación.
    Necesita saber sobre qué tema revisar la preocupación y en qué unidad dar las métricas.
    Además, se le debe pasar el dataframe conteniendo la información en crudo.
    El output es un diccionario con los valores necesarios.
    '''
    t_field='sample_size'
    concern_fields=['very','not_at_all']
    unit=unit.lower()
    people_concern_topic_data=data[data['subject'].str.contains(topic)]
    
    if unit=='absolute':
        people_concern_topic_data=build_absolute_numbers_data(concern_fields,
            t_field,people_concern_topic_data)
        
        people_very_concern=sum(
            people_concern_topic_data['very'].replace('',0).astype(float)
                )
        people_not_at_all_concern=sum(
            people_concern_topic_data['not_at_all'].replace('',0).astype(float)
                )
    
    elif unit=='percentage':
        people_very_concern=np.mean(
            people_concern_topic_data['very'].replace('',0).astype(float)
                )
        people_not_at_all_concern=np.mean(
            people_concern_topic_data['not_at_all'].replace('',0).astype(float)
                )
            
    elif unit!='percentage':
        print('La unidad escogida no es correcta. \
            Los valores permitidos son "absolute" y "percentage"')
        return 0
    
    people_distr_concern={'people_very_concern':people_very_concern,
        'people_not_at_all_concern':people_not_at_all_concern}
    
    return people_distr_concern

def do_plot_concerns(data,pic_name,topic):
    '''
    Este método crea una imagen de la gráfica sobre la distribución de las personas por su nivel de preocupación.
    Solamente necesita los datos a graficar y el nombre del gráfico.
    Además se puede personalizar el título del gráfico con la variable de entrada "topic".
    '''
    classes_name=['very','not_at_all']
    wid=0.2
    
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    
    very_bars=ax.bar(color='lightgreen',
                height=data['people_very_concern'],x=0,width=wid)
    
    not_at_all_bars=ax.bar(color='grey',
                height=data['people_not_at_all_concern'],x=1+wid,width=wid)
    
    plt.xticks([0,(1+wid)])
    ax.set_xticklabels(classes_name)
    
    plt.legend(['Muy concienciado','Nada concienciado'])
    plt.title(f'Distribución de la concienciación de la gente sobre {topic}')
    plt.savefig(pic_name)
    plt.close()

def build_poll_per_grade(data):
    '''
    Este método hace un agrupado del número de entrevistas por nota.
    Input:
        - DataFrame con los valores de las notas reescalados y el número de entrevistas por agente.
    Output:
        - DataFrame que suma el número de entrevistas por nota.
    '''
    polls_grade_mapped=build_polls_grade_mapped(data)
    poll_per_grade=polls_grade_mapped.groupby(by='grade_reclass').sum()['# of Polls']
    return poll_per_grade

def build_polls_grade_mapped(data):
    '''
    Este método modifica un campo de notas bajo nuestro estándar:
        - El campo debe contener solamente strings de los siguientes formatos:
            - Un caracter de los siguientes: a,b,c,d,f
            - Dos caracteres de la lista anterior separados por un "/" siendo el segundo el de menor valor.
            - Un caracter junto a un símbolo "-" o "+".
    El resultado será el mismo dataframe pero con un campo nuevo: grade_reclass.
    Este campo contiene los mismos valores que el orginal excepto en los casos en que el valor no fuera solo un string.
    Es decir, si se tiene un valor "A+" el nuevo campo será "A", yendo así a la nota menor más próxima.
    '''
    polls_grade_mapped=data.copy()
    grade_reclass_pd_input=[]
    for g in data['538 Grade']:
        if '/' in g:
            aux_grade_reclass=g.split('/')[1]
        else:
            aux_grade_reclass=g[0]
        grade_reclass_pd_input.append(aux_grade_reclass)
    
    polls_grade_mapped['grade_reclass']=grade_reclass_pd_input
    return polls_grade_mapped

def do_plot_polls_grade(data,pic_name):
    '''
    Este método crea una imagen de la gráfica sobre la distribución de número de entrevistas por nota.
    Solamente necesita los datos a graficar y el nombre del gráfico.
    '''
    classes_name=['A','B','C','D','F']
    indexes_bar = np.arange(len(classes_name))
    
    my_cmap = plt.cm.get_cmap('RdYlGn')
    data_color=[d/max(data.values) for d in data.values]
    colors = my_cmap(data_color)    
    
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    
    polls_grade_bars=plt.bar(color=colors,height=list(data.values),x=indexes_bar)
    ax.set_xticks(indexes_bar)
    ax.set_xticklabels(classes_name)
    
    plt.title(f'Distribución de número de entrevistas por nota')
    plt.savefig(pic_name)
    
    plt.close()
