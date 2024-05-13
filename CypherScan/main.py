import argparse
from modulos.escanerp import *
from modulos.analizarv import *
from modulos.metadatos import print_meta
from modulos.cifrado import cifrar_archivos
from modulos.webscr import scraping_web
from modulos.api import analizar_urls
from modulos.gmps import googlemaps

def main(url):
    scraping_web(url)

    print("\nIniciando el análisis de las URLs adquiridas...")
    archivo_urls = "url_img.txt"
    analizar_urls(archivo_urls)

    rutas_imagenes = [
        r"C:\Users\karla\OneDrive\Documentos\GitHub\CypherScan\modulos\IMGS",
    ]
    print_meta(rutas_imagenes)
    googlemaps()
    cifrar_archivos()

    url2 = 'ubuntu.com'
    ip = obtener_ip(url2)
    if ip:
        print(f"\nLa dirección IP de {url2} es: {ip}")
        print("\nIniciando escaneo de puertos...")
        resultados_puertos = escanear_puertos(ip)
        archivo_resultados_puertos = r'C:\Users\karla\OneDrive\Documentos\GitHub\CypherScan\resultados_puertos.txt'
        guardar_resultados(resultados_puertos, archivo_resultados_puertos)
        print(f"\nResultados de escaneo de puertos guardados en {archivo_resultados_puertos}")

        print("\nIniciando análisis de vulnerabilidades del sitio web...")
        archivo_puertos_abiertos = archivo_resultados_puertos
        puertos_abiertos = obtener_puertos_abiertos(archivo_puertos_abiertos)
        resultados_vulnerabilidades = analizar_vulnerabilidades(ip, puertos_abiertos)
        for resultado in resultados_vulnerabilidades:
            print(resultado)
    else:
        print("No se pudo obtener la IP.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script principal para análisis de seguridad web.")
    parser.add_argument("url", type=str, help="URL del sitio web a analizar")
    args = parser.parse_args()
    main(args.url)
