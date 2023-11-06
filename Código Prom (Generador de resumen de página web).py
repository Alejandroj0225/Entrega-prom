#!/usr/bin/env python
# coding: utf-8

# 1.Instalación de Transformers,importación de dependencias y cargar pipeline de resumen específica

# In[1]:


get_ipython().system('pip install transformers')

from transformers import pipeline

# Cargar el modelo de resumen de BART
resumen = pipeline("summarization", model="facebook/bart-large-cnn")


# 2. Obtención de contenido directamente de página web

# In[2]:


get_ipython().system('pip install requests beautifulsoup4')
import requests
from bs4 import BeautifulSoup
# Definir la URL del blog
URL = "https://www.xataka.com/analisis/iphone-15-pro-max-opiniones-toma-contacto-video-fotos"

# Realizar una solicitud HTTP para obtener el contenido de la página
response = requests.get(URL)

# Verificar si la solicitud fue exitosa (código de respuesta 200)
if response.status_code == 200:
    # Parsear el contenido HTML de la página con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer encabezados (h1) y párrafos (p) del blog
    encabezados = soup.find_all('h1')
    parrafos = soup.find_all('p')

    # Crear una variable para almacenar el contenido del blog
    contenido_blog = ""

    # Agregar encabezados al contenido del blog
    for h1 in encabezados:
        contenido_blog += h1.get_text() + "\n"

    # Agregar párrafos al contenido del blog
    for p in parrafos:
        contenido_blog += p.get_text() + "\n"

    # Ahora, contenido_blog contiene el contenido del blog con encabezados (h1) y párrafos (p)
else:
    # En caso de que la solicitud no sea exitosa, manejar el error
    print("Error al obtener la página:", response.status_code)

# Puedes acceder al contenido del blog en la variable contenido_blog



# In[3]:


contenido_blog


# 3. División de texto en fragmentos

# In[4]:


fragmentos = []
fragmento_actual = ""
longitud_maxima = 1500

for palabra in contenido_blog.split():
    if len(fragmento_actual) + len(palabra) + 1 <= longitud_maxima:  # +1 para el espacio
        if fragmento_actual:
            fragmento_actual += " "
        fragmento_actual += palabra
    else:
        fragmentos.append(fragmento_actual)
        fragmento_actual = palabra

if fragmento_actual:
    fragmentos.append(fragmento_actual)


# In[5]:


len(fragmentos[6].split(" "))


# In[6]:


fragmentos[0]


# 4. Resumir texto

# In[7]:


resumenes = resumen(fragmentos, max_length=120, min_length=30, do_sample=False)

# Extraer los resúmenes de los diccionarios
Ex_resumenes = [item['summary_text'] for item in resumenes]

# Compila todos los resúmenes con espacios
texto_resumen = " ".join(Ex_resumenes)


# In[8]:


texto_resumen


# 5. Guardar en un Archivo de Texto

# In[ ]:


with open('resumenblog2.txt', 'w', encoding='utf-8') as archivo:
    archivo.write(texto_resumen)

