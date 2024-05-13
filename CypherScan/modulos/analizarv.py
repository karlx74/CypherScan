import nmap

def obtener_puertos_abiertos(archivo):
    try:
        with open(archivo, 'r') as file:
            puertos_abiertos = [int(port.strip()) for port in file.read().split(',') if port.strip()]
        return puertos_abiertos
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}")
        return []

def analizar_vulnerabilidades(ip, puertos):
    scanner = nmap.PortScanner()
    try:
        resultados = []
        for puerto in puertos:
            resultado_puerto = f"Análisis de vulnerabilidades para el puerto {puerto}:"
            vulnerabilidades = scanner.scan(ip, str(puerto), arguments='-sV --script vulners')
            if 'vulners' in vulnerabilidades['scan'][ip]['tcp'][puerto]:
                for vulnerability in vulnerabilidades['scan'][ip]['tcp'][puerto]['vulners']:
                    resultado_puerto += f"\n- {vulnerability}: {vulnerabilidades['scan'][ip]['tcp'][puerto]['vulners'][vulnerability][0]['description']}"
            else:
                resultado_puerto += "No se encontraron vulnerabilidades."
            resultados.append(resultado_puerto)
        return resultados
    except nmap.nmap.PortScannerError:
        return ["Error al escanear vulnerabilidades."]
    except Exception as e:
        return [f"Ocurrió un error: {str(e)}"]
