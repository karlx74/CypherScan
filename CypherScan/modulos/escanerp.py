import socket
import nmap

def obtener_ip(url):
    try:
        ip = socket.gethostbyname(url)
        return ip
    except socket.gaierror:
        print("No se pudo resolver la dirección IP para el dominio proporcionado.")
        return None

def escanear_puertos(ip):
    scanner = nmap.PortScanner()
    try:
        scanner.scan(ip)
        results = []
        for host in scanner.all_hosts():
            results.append(f"Escaneando puertos para {host}:")
            for proto in scanner[host].all_protocols():
                results.append(f"Protocolo: {proto}")
                ports = scanner[host][proto].keys()
                for port in ports:
                    results.append(f"Puerto {port}: {scanner[host][proto][port]['state']}")
        return results
    except nmap.nmap.PortScannerError:
        return ["Error al escanear puertos."]
    except Exception as e:
        return [f"Ocurrió un error: {str(e)}"]

def guardar_resultados(resultados, archivo):
    with open(archivo, 'w') as file:
        for resultado in resultados:
            if resultado.startswith("Puerto"):
                # Extraer el número del puerto de la cadena
                numero_puerto = resultado.split(" ")[1].split(":")[0]
                file.write(numero_puerto + ', ')