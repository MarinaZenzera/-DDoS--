import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def load_data(filename):
    """Загрузка данных из файла Excel."""
    try:
        data = pd.read_excel(filename)
        data['Time'] = pd.to_datetime(data['Time'], unit='s')
        return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return None

def analyze_data(data):
    """Анализ данных."""
    if data is None:
        return None

    results = {
        'total_packets': len(data),
        'total_traffic': data['Packet Size'].sum(),
        'top_src_ips': data['Src IP'].value_counts().head(10).to_dict(),
        'top_dst_ips': data['Dst IP'].value_counts().head(10).to_dict(),
        'top_src_ports': data['Src Port'].value_counts().head(10).to_dict(),
        'top_dst_ports': data['Dst Port'].value_counts().head(10).to_dict(),
        'protocol_counts': data['Protocol'].value_counts().to_dict()
    }
    return results


def plot_time_distribution(data, output_dir):
    """График распределения пакетов по времени."""
    if data is None:
        return

    time_counts = data.groupby(pd.Grouper(key='Time', freq='1S'))['Packet Size'].count()
    plt.figure(figsize=(10, 6))
    plt.plot(time_counts.index, time_counts.values, marker='o', linestyle='-', markersize=2)
    plt.title('Распределение пакетов по времени')
    plt.xlabel('Время')
    plt.ylabel('Количество пакетов')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'time_distribution.png'))
    plt.close()


def plot_distribution(data, col, top_n, title, filename, output_dir):
    """График распределения (IP или порты)."""
    if data is None:
        return

    counts = data[col].value_counts().head(top_n)
    plt.figure(figsize=(10, 6))
    counts.plot(kind='bar', color='skyblue')
    plt.title(title)
    plt.xlabel(title.split(' ')[0] )
    plt.ylabel('Количество пакетов')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def plot_packet_size_distribution(data, output_dir):
    if data is None:
        return
    plt.figure(figsize=(10,6))
    plt.hist(data['Packet Size'], bins=50, color='coral')
    plt.title('Распределение размеров пакетов')
    plt.xlabel('Размер пакета (байты)')
    plt.ylabel('Количество пакетов')
    plt.savefig(os.path.join(output_dir, 'packet_size_distribution.png'))
    plt.close()


def main():
    """Основная функция."""
    parser = argparse.ArgumentParser(description='Анализ данных DDoS-атаки.')
    parser.add_argument('filename', help='Имя файла Excel с данными.')
    parser.add_argument('--top_n', type=int, default=10, help='Количество топ-N значений для отображения.')
    parser.add_argument('--output_dir', default='output', help='Директория для сохранения графиков.')
    args = parser.parse_args()

    # Создаем директорию для выходных файлов, если её нет
    os.makedirs(args.output_dir, exist_ok=True)

    data = load_data(args.filename)
    if data is None:
      return

    results = analyze_data(data)
    if results is None:
      return

    print("Общая информация о данных:")
    print(data.info())
    print("\nПервые 5 строк данных:")
    print(data.head())
    print(f"\nОбщее количество пакетов: {results['total_packets']}")
    print(f"\nОбщий объем трафика: {results['total_traffic']} байт")
    print("\nТоп", args.top_n, "IP-адресов источника:", results['top_src_ips'])
    print("\nТоп", args.top_n, "IP-адресов назначения:", results['top_dst_ips'])
    print("\nТоп", args.top_n, "портов источника:", results['top_src_ports'])
    print("\nТоп", args.top_n, "портов назначения:", results['top_dst_ports'])
    print("\nКоличество пакетов по протоколам:", results['protocol_counts'])


    plot_time_distribution(data, args.output_dir)
    plot_distribution(data, 'Src IP', args.top_n, 'Топ-N IP-адресов источника', 'src_ip_distribution.png', args.output_dir)
    plot_distribution(data, 'Dst IP', args.top_n, 'Топ-N IP-адресов назначения', 'dst_ip_distribution.png', args.output_dir)
    plot_distribution(data, 'Src Port', args.top_n, 'Топ-N портов источника', 'src_port_distribution.png', args.output_dir)
    plot_distribution(data, 'Dst Port', args.top_n, 'Топ-N портов назначения', 'dst_port_distribution.png', args.output_dir)
    plot_packet_size_distribution(data, args.output_dir)

    print(f"\nГрафики сохранены в директорию: {args.output_dir}")


if __name__ == "__main__":
    main()
