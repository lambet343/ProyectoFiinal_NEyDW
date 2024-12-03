import requests
from bs4 import BeautifulSoup
import json

# URL de la página que deseas analizar (en este caso, la página de paquetes de eventos)
url = "https://www.salonjardineventos.com/paquetes/"

# Encabezados para la solicitud (esto simula una solicitud de un navegador para evitar bloqueos)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# Hacer una solicitud GET a la página con los encabezados especificados
response = requests.get(url, headers=headers)

# Verificar que la solicitud fue exitosa (código de estado 200 significa éxito)
if response.status_code == 200:
    # Parsear el contenido HTML de la página usando BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar los elementos HTML específicos que contienen la información de los paquetes
    # Esto se hace buscando etiquetas específicas (en este caso, h3, ul y p)
    paquetes = soup.find_all('h3')  # Selector para los títulos de los paquetes (nombres)
    descripciones = soup.find_all('ul')  # Selector para las descripciones de los paquetes
    precios = soup.find_all('p', class_='precio')  # Selector para los precios de los paquetes

    # Crear una lista vacía para almacenar los datos recolectados
    datos_paquetes = []

    # Extraer los datos de los paquetes: nombre, descripción y precio
    for i, paquete in enumerate(paquetes):
        # Limpiar y obtener el texto de cada nombre de paquete
        paquete_nombre = paquete.text.strip()
        # Obtener la descripción del paquete, con un chequeo para asegurarse de que exista
        paquete_descripcion = descripciones[i].text.strip() if i < len(descripciones) else "No disponible"
        # Obtener el precio, limpiando símbolos y comas, si existe
        paquete_precio = precios[i].text.strip().replace('$', '').replace(',', '') if i < len(precios) else "No disponible"

        # Añadir los datos extraídos a la lista de paquetes
        datos_paquetes.append({
            "nombre": paquete_nombre,
            "descripcion": paquete_descripcion,
            "precio": paquete_precio
        })

    # Guardar los datos extraídos en un archivo JSON en formato legible
    with open("paquetes.json", "w", encoding="utf-8") as file:
        json.dump(datos_paquetes, file, ensure_ascii=False, indent=4)

    # Mensaje que indica que los datos se han guardado correctamente
    print("Datos guardados en paquetes.json")
else:
    # Si la solicitud no es exitosa, imprime el código de estado del error
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
