import webbrowser

def abrir_google_maps(latitud, longitud):
    # Construir la URL de Google Maps con las coordenadas proporcionadas
    url = f"https://www.google.com/maps/search/?api=1&query={latitud},{longitud}"

    # Abrir Google Maps en el navegador predeterminado
    webbrowser.open(url)

def preguntar_abrir_google_maps(numero_ubicacion):
    respuesta = input(f"¿Deseas abrir Google Maps para ver la ubicación {numero_ubicacion}? (y/n): ")
    if respuesta.lower() == 'y':
        return True
    else:
        return False

def googlemaps():
    # Ruta del archivo de metadatos
    ruta_archivo = r"C:\Users\karla\OneDrive\Documentos\GitHub\PROGCIB\modulos\metadatos\gpsmetadatos.txt"

    try:
        with open(ruta_archivo, "r") as archivo:
            # Inicializar el contador de ubicaciones
            numero_ubicacion = 1

            # Leer cada línea del archivo
            for linea in archivo:
                # Buscar la cadena de coordenadas en la línea
                if "Lat:" in linea and "Lng:" in linea:
                    # Extraer las coordenadas de latitud y longitud
                    latitud = linea.split("Lat:")[1].split(",")[0].strip()
                    longitud = linea.split("Lng:")[1].strip()

                    # Preguntar al usuario si desea abrir Google Maps para esta ubicación
                    if preguntar_abrir_google_maps(numero_ubicacion):
                        abrir_google_maps(latitud, longitud)

                    # Incrementar el contador de ubicaciones
                    numero_ubicacion += 1

    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")