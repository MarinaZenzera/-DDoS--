from scapy.all import *
from openpyxl import Workbook

# Захват трафика
packets = rdpcap('dump3.pcapng')

# Создание нового Excel-файла
wb = Workbook()
ws = wb.active  # Активный лист

# Заголовок Excel-файла
ws.append(["Time", "Src IP", "Dst IP", "Src Port", "Dst Port", "Protocol", "Packet Size"])

# Обработка каждого пакета
for packet in packets:
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto
        packet_size = len(packet)
        
        # Определение портов для TCP/UDP
        if TCP in packet:
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif UDP in packet:
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        else:
            src_port, dst_port = None, None
        
        # Запись данных в Excel
        ws.append([packet.time, src_ip, dst_ip, src_port, dst_port, protocol, packet_size])

# Сохранение файла
wb.save('ddos_data.xlsx')

print("Файл ddos_data.xlsx успешно создан.")
