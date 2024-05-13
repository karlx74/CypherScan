import os
import requests
from lxml import html
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename="scraping.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class Scraping:
    def __init__(self, url):
        self.url = url

    def download_file(self, url, folder):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_name = url.split("/")[-1]
                file_path = os.path.join(folder, file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                return file_path
            else:
                logging.error(
                    f"No se pudo descargar el archivo de {url}. Estado de la respuesta: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error al descargar el archivo de {url}: {e}")
            return None

    def scraping_beautiful_soup(self):
        try:
            print(f"Obteniendo imágenes de {self.url}")
            response = requests.get(self.url)
            bs = BeautifulSoup(response.text, 'lxml')

            # Crear directorio para guardar imágenes
            os.makedirs("imagenes", exist_ok=True)

            image_paths = []

            # Descargar y guardar imágenes
            for tag_image in bs.find_all("img"):
                if not tag_image['src'].startswith("http"):
                    download_url = self.url + tag_image['src']
                else:
                    download_url = tag_image['src']

                image_path = self.download_file(download_url, "imagenes")
                if image_path:
                    image_paths.append(download_url)

            # Guardar rutas de imágenes en un archivo
            with open("url_img.txt", "w", encoding="utf-8") as file:
                for path in image_paths:
                    file.write(path + "\n")

        except Exception as e:
            logging.error(f"Error conexión con {self.url}: {e}")

    def scraping_images(self):
        print(f"\nObteniendo imágenes de la url {self.url}")

        try:
            response = requests.get(self.url)
            parsed_body = html.fromstring(response.text)

            # Expresión regular para obtener imágenes
            images = parsed_body.xpath('//img/@src')

            # Crear directorio para guardar imágenes
            os.makedirs("imagenes", exist_ok=True)

            image_paths = []

            # Descargar y guardar imágenes
            for image in images:
                if not image.startswith("http"):
                    download_url = self.url + image
                else:
                    download_url = image

                image_path = self.download_file(download_url, "imagenes")
                if image_path:
                    image_paths.append(download_url)

            # Guardar rutas de imágenes en un archivo
            with open("url_img.txt", "w", encoding="utf-8") as file:
                for path in image_paths:
                    file.write(path + "\n")

        except Exception as e:
            logging.error(f"Error conexión con {self.url}: {e}")

    def scraping_pdf(self):
        print(f"\nObteniendo PDFs de {self.url}")

        try:
            response = requests.get(self.url)
            parsed_body = html.fromstring(response.text)

            # Expresión regular para obtener PDFs
            pdfs = parsed_body.xpath('//a[@href[contains(., ".pdf")]]/@href')

            # Crear directorio para guardar PDFs
            os.makedirs("pdfs", exist_ok=True)

            pdf_paths = []

            # Descargar y guardar PDFs
            for pdf in pdfs:
                if not pdf.startswith("http"):
                    download_url = self.url + pdf
                else:
                    download_url = pdf

                pdf_path = self.download_file(download_url, "pdfs")
                if pdf_path:
                    pdf_paths.append(download_url)

            # Guardar rutas de PDFs en un archivo
            with open("url_pdf.txt", "w", encoding="utf-8") as file:
                for path in pdf_paths:
                    file.write(path + "\n")

        except Exception as e:
            logging.error(f"Error conexión con {self.url}: {e}")

def scraping_web(url):
    scraper = Scraping(url)
    scraper.scraping_beautiful_soup()
    scraper.scraping_images()
    scraper.scraping_pdf()