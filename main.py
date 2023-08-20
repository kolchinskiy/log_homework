import re
import os
import json
from collections import Counter


def analyze_log(log_path):
    # Шаблон для разбора строки лога
    log_pattern = re.compile(
        r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<url>\S+) .*?" '
        r'(?P<status>\d+) (?P<bytes>\d+) ".*?" ".*?" (?P<duration>\d+)')

    # Счетчики
    total_requests = 0
    method_counter = Counter()
    ip_counter = Counter()
    longest_requests = []

    # Чтение и анализ файла
    with open(log_path, 'r') as log_file:
        for line in log_file:
            match = log_pattern.match(line)
            if match:
                total_requests += 1
                method = match.group('method')
                ip = match.group('ip')
                duration = int(match.group('duration'))
                url = match.group('url')
                status = match.group('status')

                method_counter[method] += 1
                ip_counter[ip] += 1
                longest_requests.append({
                    'method': method,
                    'url': url,
                    'ip': ip,
                    'duration': duration,
                    'timestamp': match.group('timestamp'),
                    'status': status
                })

    # Получение топ 3 IP адресов
    top_ips = ip_counter.most_common(3)

    # Получение топ 3 самых долгих запросов
    longest_requests.sort(key=lambda x: x['duration'], reverse=True)
    top_longest_requests = longest_requests[:3]

    return {
        'total_requests': total_requests,
        'method_stats': method_counter,
        'top_ips': top_ips,
        'top_longest_requests': top_longest_requests
    }


def main():
    # Запрос пути к файлу или директории
    log_path = input("Введите путь к файлу или директории с логами: ")
    if os.path.isfile(log_path):
        result = analyze_log(log_path)
        output_path = os.path.splitext(log_path)[0] + '_analysis.json'
        with open(output_path, 'w') as output_file:
            json.dump(result, output_file, indent=4)
        print("Анализ выполнен. Результаты сохранены в", output_path)
    elif os.path.isdir(log_path):
        log_files = [f for f in os.listdir(log_path) if f.endswith('.log')]
        for log_file in log_files:
            log_file_path = os.path.join(log_path, log_file)
            result = analyze_log(log_file_path)
            output_path = os.path.splitext(log_file_path)[0] + '_analysis.json'
            with open(output_path, 'w') as output_file:
                json.dump(result, output_file, indent=4)
            print("Анализ выполнен. Результаты сохранены в", output_path)
    else:
        print("Указанный путь не является действительным файлом или директорией.")


if __name__ == "__main__":
    main()
