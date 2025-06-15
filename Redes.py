import math
from typing import List, Tuple, Optional

# Variables
MIN_PREFIX: int = 1
MAX_PREFIX: int = 32
MENU_BORDER: str = '-' * 64
MENU_OPTIONS: List[str] = [
    "| 1. Iniciar el Generador de Subredes VLSM                     |",
    "| 2. Conversor a máscara Wildcard                              |",
    "| 3. Calcular Dirección de Red                                 |"
]

def validar_octeto(octeto: int) -> bool:
    return 0 <= octeto <= 255

def validar_prefijo(prefijo: int) -> bool:
    return MIN_PREFIX <= prefijo <= MAX_PREFIX

def obtener_mascara_decimal(prefijo: int) -> List[int]:
    mascara = []
    for i in range(4):
        if prefijo >= 8:
            mascara.append(255)
            prefijo -= 8
        elif prefijo > 0:
            mascara.append(256 - 2 ** (8 - prefijo))
            prefijo = 0
        else:
            mascara.append(0)
    return mascara

def obtener_mascara_inversa(mascara: List[int]) -> List[int]:
    return [255 - octeto for octeto in mascara]

def calcular_hosts_disponibles(prefijo: int) -> int:
    """Calcula el número máximo de hosts disponibles en la red base"""
    bits_hosts = 32 - prefijo
    return (2 ** bits_hosts) - 2  # Restamos 2 para dirección de red y broadcast

def solicitar_prefijo_wildcard() -> int:
    while True:
        try:
            print(MENU_BORDER)
            print("|                  Conversor a máscara Wildcard                 |")
            print(MENU_BORDER)
            prefijo = int(input(f"Ingrese el número de la máscara (Ejemplo: /{MAX_PREFIX}= {MAX_PREFIX}): "))
            if validar_prefijo(prefijo):
                break
            print("\n❌ Ingrese una Máscara válida entre 1 y 32.")
        except ValueError:
            print("\n❌ Ingrese una Máscara válida entre 1 y 32.")
    print(MENU_BORDER)
    return prefijo

def solicitar_ip_y_prefijo() -> Tuple[List[int], int]:
    while True:
        try:
            print(MENU_BORDER)
            print("|                  Generador de Subredes VLSM                  |")
            print(MENU_BORDER)
            ip_completa = input("Ingrese la Dirección IP (Ejemplo: 172.20.192.0): ")
            IPinicial = list(map(int, ip_completa.split(".")))
            if len(IPinicial) == 4 and all(validar_octeto(octeto) for octeto in IPinicial):
                break
            print("\n❌ Ingrese una IP válida.")
        except ValueError:
            print("\n❌ Ingrese una IP válida.")

    while True:
        try:
            prefijo = int(input(f"Ingrese el número de la máscara base (Ejemplo: /{MAX_PREFIX}= {MAX_PREFIX}): "))
            if validar_prefijo(prefijo):
                break
            print("\n❌ Ingrese una Máscara válida entre 1 y 32.")
        except ValueError:
            print("\n❌ Ingrese una Máscara válida entre 1 y 32.")

    print(MENU_BORDER)
    print(f"🌐 La Dirección IP base es: {'.'.join(map(str, IPinicial))}/{prefijo}")
    
    hosts_disponibles = calcular_hosts_disponibles(prefijo)
    mascara_decimal = obtener_mascara_decimal(prefijo)
    print(f"📍 Máscara de subred: {'.'.join(map(str, mascara_decimal))}")
    print(f"📍 Hosts disponibles en la red base: {hosts_disponibles:,} usuarios")
    print(MENU_BORDER)
    return IPinicial, prefijo

def solicitar_segmentos_y_hosts() -> List[Tuple[int, int]]:
    while True:
        try:
            j = int(input("Cuantos Segmentos + PTP desea tener: "))
            if j > 0:
                break
            print("\n❌ Ingrese un valor correcto. Vuelva a intentarlo...")
        except ValueError:
            print("\n❌ Ingrese un valor correcto. Vuelva a intentarlo...")
    
    hosts = []
    for i in range(j):
        while True:
            try:
                h = int(input(f"Cantidad de Hosts en Segmento {i+1}: "))
                if h >= 0:
                    hosts.append((i+1, h))
                    break
                print("\n❌ Ingrese un valor correcto. Vuelva a intentarlo...")
            except ValueError:
                print("\n❌ Ingrese un valor correcto. Vuelva a intentarlo...")
    
    hosts.sort(key=lambda x: x[1], reverse=True)
    print(MENU_BORDER)
    print("🔹Las Subredes ordenadas de mayor a menor son:")
    for seg, h in hosts:
        print(f"📍Segmento {seg}: {h} host")
    print(MENU_BORDER)
    print('\n')
    return hosts

def calcular_subredes(hosts: List[Tuple[int, int]], IPinicial: List[int], prefijo: int) -> None:
    total_ips = 0
    for seg_num, h in hosts:
        bits = math.ceil(math.log2(h + 2))
        nuevo_prefijo = 32 - bits
        num_ips = 2 ** bits
        red = total_ips
        broadcast = total_ips + num_ips - 1
        primer_host = red + 1
        ultimo_host = broadcast - 1

        print(f"📍SEGMENTO {seg_num}")
        ip_red = calcular_ip(IPinicial, red)
        print(f"La Direccion de Red es: {'.'.join(map(str, ip_red))}/{nuevo_prefijo}")

        ip_primer = calcular_ip(IPinicial, primer_host)
        ip_ultimo = calcular_ip(IPinicial, ultimo_host)
        print(f"El Rango IP's útiles es: {'.'.join(map(str, ip_primer))} - {'.'.join(map(str, ip_ultimo))}")

        ip_broadcast = calcular_ip(IPinicial, broadcast)
        print(f"La Direc Broadcast es: {'.'.join(map(str, ip_broadcast))}")

        mascara_decimal = obtener_mascara_decimal(nuevo_prefijo)
        print("La Máscara de Subred es: " + '.'.join(map(str, mascara_decimal)))
        print('\n')

        total_ips += num_ips

def calcular_ip(ip_base: List[int], n: int) -> List[int]:
    ip = ip_base[:]
    for i in range(3, -1, -1):
        ip[i] += n % 256
        n //= 256
    return ip

def convertir_a_wildcard() -> None:
    while True:
        prefijo = solicitar_prefijo_wildcard()
        mascara_decimal = obtener_mascara_decimal(prefijo)
        mascara_inversa = obtener_mascara_inversa(mascara_decimal)
        
        print('\n' + MENU_BORDER)
        print("🔹 Resultados del Conversor:")
        print(f"📍 Máscara: /{prefijo}")
        print(f"📍 Máscara de Subred: {'.'.join(map(str, mascara_decimal))}")
        print(f"📍 Máscara Wildcard: {'.'.join(map(str, mascara_inversa))}")
        print(MENU_BORDER + '\n')
        
        print("Presione 'M' para volver al menú principal o ENTER para continuar...")
        opcion = input().upper()
        if opcion == 'M':
            return

def solicitar_ip_y_mascara() -> Tuple[List[int], int]:
    while True:
        try:
            print(MENU_BORDER)
            print("|                  Calcular Dirección de Red                   |")
            print(MENU_BORDER)
            ip_completa = input("Ingrese la Dirección IP (Ejemplo: 192.168.1.100): ")
            IP = list(map(int, ip_completa.split(".")))
            if len(IP) == 4 and all(validar_octeto(octeto) for octeto in IP):
                break
            print("\n❌ Ingrese una IP válida.")
        except ValueError:
            print("\n❌ Ingrese una IP válida.")

    while True:
        try:
            prefijo = int(input(f"Ingrese el número de la máscara (Ejemplo: /{MAX_PREFIX}= {MAX_PREFIX}): "))
            if validar_prefijo(prefijo):
                break
            print("\n❌ Ingrese una Máscara válida entre 1 y 32.")
        except ValueError:
            print("\n❌ Ingrese una Máscara válida entre 1 y 32.")

    print(MENU_BORDER)
    return IP, prefijo

def calcular_direccion_red(ip: List[int], prefijo: int) -> List[int]:
    """Calcula la dirección de red aplicando la máscara de subred"""
    mascara = obtener_mascara_decimal(prefijo)
    direccion_red = []
    for i in range(4):
        direccion_red.append(ip[i] & mascara[i])
    return direccion_red

def calcular_direccion_broadcast(ip: List[int], prefijo: int) -> List[int]:
    """Calcula la dirección de broadcast"""
    mascara = obtener_mascara_decimal(prefijo)
    mascara_inversa = obtener_mascara_inversa(mascara)
    direccion_red = calcular_direccion_red(ip, prefijo)
    broadcast = []
    for i in range(4):
        broadcast.append(direccion_red[i] | mascara_inversa[i])
    return broadcast

def calcular_direccion_red_completa() -> None:
    while True:
        ip, prefijo = solicitar_ip_y_mascara()
        
        # Calcular dirección de red
        direccion_red = calcular_direccion_red(ip, prefijo)
        
        # Calcular máscara de subred
        mascara_decimal = obtener_mascara_decimal(prefijo)
        
        # Calcular máscara wildcard
        mascara_inversa = obtener_mascara_inversa(mascara_decimal)
        
        # Calcular dirección de broadcast
        direccion_broadcast = calcular_direccion_broadcast(ip, prefijo)
        
        # Calcular primer y último host
        primer_host = direccion_red[:]
        primer_host[3] += 1
        
        ultimo_host = direccion_broadcast[:]
        ultimo_host[3] -= 1
        
        print(f"🌐 IP ingresada: {'.'.join(map(str, ip))}/{prefijo}")
        print(MENU_BORDER)
        print("🔹 Resultados del Cálculo:")
        print(f"📍 Dirección de Red: {'.'.join(map(str, direccion_red))}/{prefijo}")
        print(f"📍 Máscara de Subred: {'.'.join(map(str, mascara_decimal))}")
        print(f"📍 Máscara Wildcard: {'.'.join(map(str, mascara_inversa))}")
        print(f"📍 El Rango IP's útiles es: {'.'.join(map(str, primer_host))} - {'.'.join(map(str, ultimo_host))}")
        print(f"📍 Dirección Broadcast: {'.'.join(map(str, direccion_broadcast))}")
        print(f"🚀 Para el OSPF: network {'.'.join(map(str, direccion_red))} {'.'.join(map(str, mascara_inversa))} area 0")
        print(MENU_BORDER + '\n')
        
        print("Presione 'M' para volver al menú principal o ENTER para continuar...")
        opcion = input().upper()
        if opcion == 'M':
            return

def mostrar_menu() -> str:
    while True:
        try:
            print(MENU_BORDER)
            for opcion in MENU_OPTIONS:
                print(opcion)
            print(MENU_BORDER[:-1])
            opcion = input("\nSeleccione una opción (1-3): ")
            if opcion in ['1', '2', '3']:
                return opcion
            print("\n❌ Por favor, seleccione una opción válida (1-3)")
        except ValueError:
            print("\n❌ Por favor, seleccione una opción válida (1-3)")

def main() -> None:
    while True:
        opcion = mostrar_menu()
        if opcion == '1':
            IPinicial, prefijo = solicitar_ip_y_prefijo()
            hosts = solicitar_segmentos_y_hosts()
            calcular_subredes(hosts, IPinicial, prefijo)
            print("Programa terminado. ¡Hasta pronto!")
            break
        elif opcion == '2':
            convertir_a_wildcard()
            continue
        elif opcion == '3':
            calcular_direccion_red_completa()
            continue

if __name__ == "__main__":
    main()