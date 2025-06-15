import math
def solicitar_ip_y_prefijo():
    while True:
        try:
            print(' --------------------------------------------------------------')
            print("|                  Generador de Subredes VLSM                  |")
            print(' --------------------------------------------------------------')
            ip_completa = input("Ingrese la Dirección IP (Ejemplo: 172.20.192.0): ")
            IPinicial = list(map(int, ip_completa.split(".")))
            if len(IPinicial) == 4 and all(0 <= octeto <= 255 for octeto in IPinicial):
                break
            else:
                print("\nIngrese una IP válida.")
        except ValueError:
            print("\nIngrese una IP válida.")

    while True:
        try:
            prefijo = int(input("Ingrese el número de la máscara base (Ejemplo: /32= 32): "))
            if 0 < prefijo <= 32:
                break
            else:
                print("\nIngrese una Máscara válida entre 1 y 32.")
        except ValueError:
            print("\nIngrese una Máscara válida entre 1 y 32.")

    print('----------------------------------------------------------------')
    print(f"🌐 La Dirección IP base es: {'.'.join(map(str, IPinicial))}/{prefijo}                   🌐")
    print('----------------------------------------------------------------')
    return IPinicial, prefijo

def solicitar_segmentos_y_hosts():
    while True:
        try:
            j = int(input("Cuantos Segmentos + PTP desea tener: "))
            if j > 0:
                break
            else:
                print("\nIngrese un valor correcto. Vuelva a intentarlo...")
        except ValueError:
            print("\nIngrese un valor correcto. Vuelva a intentarlo...")
    hosts = []
    for i in range(j):
        while True:
            try:
                h = int(input(f"Cantidad de Hosts en Segmento {i+1}: "))
                if h >= 0:
                    hosts.append((i+1, h))
                    break
                else:
                    print("\nIngrese un valor correcto. Vuelva a intentarlo...")
            except ValueError:
                print("\nIngrese un valor correcto. Vuelva a intentarlo...")
    hosts.sort(key=lambda x: x[1], reverse=True)
    print('----------------------------------------------------------------')
    print("🔹Las Subredes ordenadas de mayor a menor son:")
    for seg, h in hosts:
        print(f"📍Segmento {seg}: {h} host")
    print('----------------------------------------------------------------')
    print('\n')
    return hosts

def obtener_mascara_decimal(prefijo):
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

def calcular_subredes(hosts, IPinicial, prefijo):
    ip_actual = IPinicial[:]
    total_ips = 0
    for seg_num, h in hosts:
        bits = math.ceil(math.log2(h + 2))
        nuevo_prefijo = 32 - bits
        num_ips = 2 ** bits
        red = total_ips
        broadcast = total_ips + num_ips - 1
        primer_host = red + 1
        ultimo_host = broadcast - 1
        def int_to_ip(ip_base, n):
            ip = ip_base[:]
            for i in range(3, -1, -1):
                ip[i] += n % 256
                n //= 256
            return ip

        print(f"📍SEGMENTO {seg_num}")
        ip_red = int_to_ip(IPinicial, red)
        print("La Direccion de Red es: ", end="")
        print(f"{'.'.join(map(str, ip_red))}/{nuevo_prefijo}")

        ip_primer = int_to_ip(IPinicial, primer_host)
        ip_ultimo = int_to_ip(IPinicial, ultimo_host)
        print("El Rango IP’s útiles es: ", end="")
        print(f"{'.'.join(map(str, ip_primer))} - {'.'.join(map(str, ip_ultimo))}")

        ip_broadcast = int_to_ip(IPinicial, broadcast)
        print("La Direc Broadcast es: ", end="")
        print(f"{'.'.join(map(str, ip_broadcast))}")

        mascara_decimal = obtener_mascara_decimal(nuevo_prefijo)
        print("La máscara de Subred es: " + '.'.join(map(str, mascara_decimal)))
        print('\n')

        total_ips += num_ips

def main():
    IPinicial, prefijo = solicitar_ip_y_prefijo()
    hosts = solicitar_segmentos_y_hosts()
    calcular_subredes(hosts, IPinicial, prefijo)

if __name__ == "__main__":
    main()