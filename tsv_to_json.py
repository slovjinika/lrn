import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    """
    Преобразует CSV файл с разделителем-табуляцией в JSON файл.

    Args:
        csv_file_path: Путь к CSV файлу.
        json_file_path: Путь к JSON файлу.
    """
    data = []
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')  # Указываем разделитель-табуляцию
        for row in csv_reader:
            data.append(row)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

# Пример использования:
csv_file = 'input.tsv'  # Замените на ваш TSV файл (TSV = Tab Separated Values)
json_file = 'output.json'
csv_to_json(csv_file, json_file)

print(f"Файл {csv_file} успешно преобразован в {json_file}")
