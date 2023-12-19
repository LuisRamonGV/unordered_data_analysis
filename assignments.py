# -*- coding: utf-8 -*-
"""
Practica 3
Autor: Garcia Vazquez Luis Ramon
Curso: Minería de Datoso
Fecha: 08-12-2023
Descripción: Este programa procesa dos conjuntos de datos que incluyen información 
sobre materias, palabras clave y documentos de texto. Utiliza el algoritmo de Jaccard 
para identificar las similitudes entre cada conjunto de palabras clave y 
los documentos asociados. Realiza cálculos de precisión y recall para evaluar la 
calidad de las coincidencias encontradas. Finalmente, genera un archivo CSV que resume los 
resultados obtenidos en este proceso.
"""
from nltk.corpus import stopwords
import pandas as pd
import re

# Función para cargar un DataFrame desde un archivo CSV
def dataframes(var):    
    w_d = 'C:/Users/luisr/OneDrive - Universidad de Guanajuato/Documentos/DM/Code/Assignment_3/'
    f_i = w_d + var
    return pd.read_csv(f_i)

# Función para procesar un documento de texto
def process_document(pub):
    
    # Función para quitar acentos de un token
    def no_accent(token):
        return token.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

    # Obtener la lista precompilada de stopwords de NLTK para español
    s_w = stopwords.words('spanish')
    
    # Convertir la lista de stopwords a un conjunto para una búsqueda más eficiente
    s_w = set(s_w)
    
    # Tokenizar y procesar el texto
    pub = re.findall('\w+', pub.lower())
    pub = [no_accent(token) for token in pub
           if token.isalpha()
           and (len(token) >= 3 and len(token) <= 20)
           and token not in s_w]
    
    return pub

# Función para calcular la similitud de Jaccard entre dos conjuntos
def jaccard(a, b):
    set_a = set(a)
    set_b = set(b)
    num = len(set_a.intersection(set_b))
    den = len(set_a.union(set_b))
    jac = num / den
    return jac

# Cargar los datos de documentos y palabras clave desde archivos CSV
df = dataframes('/data.csv')
data = df['texto'].tolist()
d_d = [process_document(i) for i in data]
d_m = df['materia'].tolist()

dg = dataframes('/keywords.csv')
data_k = dg['keywords'].tolist()
k_d = [process_document(i) for i in data_k]                                           
k_m = dg['materia'].tolist()

# Lista para almacenar los resultados
s_j = []

# Calcular similitud de Jaccard y encontrar los 5 documentos más similares para cada conjunto de palabras clave
for i, k in enumerate(k_d):
    m_t = []
    for j, doc in enumerate(d_d):
        m_t.append([j, jaccard(set(k), set(doc))])   
    
    m_t_5 = [item[0] for item in sorted(m_t, key=lambda x: x[1], reverse=True)[:5]]
   
    s_j.append([k, k_m[i], m_t_5])

# Listas para almacenar precisión y recall
prec = []
rec = []

# Calcular precisión y recall para cada conjunto de palabras clave
for i, item in enumerate(s_j):
    # Encontrar las materias de los documentos más similares
    c = [d_m[indice] for indice in item[2]]
    item.append(c)
    
    # Contar la cantidad de veces que la materia real aparece en las materias de los documentos similares
    countt = item[3].count(item[1])
    
    # Calcular precisión y recall
    precision = countt / 5
    recall = countt / 20
    
    # Imprimir resultados
    print(f'Doc {i}\tPrecision: {precision:.1f} \tRecall:{recall:.2f}')
    
    # Almacenar precisiones y recalls
    prec.append(precision)
    rec.append(recall)

# Calcular promedio de precisiones y recalls
avg_precision = sum(prec) / len(prec) if len(prec) > 0 else 0
avg_recall = sum(rec) / len(rec) if len(rec) > 0 else 0

# Imprimir promedios
print(f'\nAvg Precision: {avg_precision:.3f}')
print(f'Avg Recall: {avg_recall:.3f}')

# Escribir resultados en un archivo CSV
archivo = 'results.csv'
with open(archivo, 'w', encoding='utf-8') as writer:  
    writer.write('palabras_clave;materia;indices;materias\n')

    for item in s_j:    
        # Convertir listas a cadenas separadas por comas
        keywords = ','.join(map(str, item[0]))
        indices = ','.join(map(str, item[2]))
        materias = ','.join(map(str, item[3]))

        # Escribir línea en el archivo CSV
        linea = f'{keywords};{item[1]};{indices};[{materias}]\n'
        writer.write(linea)
