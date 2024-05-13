from PIL.ExifTags import TAGS
from PIL import Image
import os

def decode_gps_info(exif):
    gpsinfo = {}
    if 'GPSInfo' in exif:
        # Parse geo references.
        Nsec = exif['GPSInfo'][2][2]
        Nmin = exif['GPSInfo'][2][1]
        Ndeg = exif['GPSInfo'][2][0]
        Wsec = exif['GPSInfo'][4][2]
        Wmin = exif['GPSInfo'][4][1]
        Wdeg = exif['GPSInfo'][4][0]
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][1] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat": Lat, "Lng": Lng}

def get_exif_metadata(image_path):
    ret = {}
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    decode_gps_info(ret)
    return ret
    
def save_metadata_to_txt(metadata, file_path):
    with open(file_path, 'a') as file:
        file.write(metadata)

def print_meta(image_folders):
    for image_folder in image_folders:
        print(f"\nProcesando imágenes en: {image_folder}")
        if not os.path.isdir(image_folder):
            print(f"La ruta {image_folder} no es un directorio válido.")
            continue
        os.chdir(image_folder)
        output_folder = os.path.join(os.path.dirname(image_folder), "metadatos")
        os.makedirs(output_folder, exist_ok=True)
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                try:
                    exif = get_exif_metadata(name)
                    for metadata in ['Model', 'DateTimeOriginal', 'DateTimeDigitized']:
                        if metadata in exif:
                            metadata_string = "Metadata: %s - Value: %s \n" % (metadata, exif[metadata])
                            save_metadata_to_txt(metadata_string, os.path.join(output_folder, "metadatos.txt"))
                    if 'GPSInfo' in exif:
                        gps_metadata_string = "Metadata: GPSInfo - Lat: %s, Lng: %s \n" % (exif['GPSInfo']['Lat'], exif['GPSInfo']['Lng'])
                        save_metadata_to_txt(gps_metadata_string, os.path.join(output_folder, "gpsmetadatos.txt"))
                except Exception as e:
                    print("Error: ", e)

        print(f"\nMetadatos de {image_folder} guardados correctamente.")