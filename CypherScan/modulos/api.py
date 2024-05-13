from virus_total_apis import PublicApi
from key.key_api import api_key
import os
import time

def analizar_urls(archivo_urls):
    api = PublicApi(api_key)
    urls_seguras = []

    with open(archivo_urls, "r") as file:
        for url in file:
            url = url.strip()
            response = api.get_url_report(url)
            time.sleep(3)

            try:
                if response["response_code"] == 200:
                    if "positives" in response["results"]:
                        if response["results"]["positives"] > 0:
                            print(f"La URL {url} es maliciosa.")
                            time.sleep(3)
                            print("Procederemos a eliminar el archivo asociado.")
                            os.remove(archivo_urls)
                        else:
                            print(f"La URL {url} es segura.")
                            urls_seguras.append(url)
                            with open("urls_seguras.txt", "a") as output_file:
                                output_file.write(f"{url}\n")
            except Exception as e:
                print(f"Ocurrió un error al procesar la URL {url}: {e}")