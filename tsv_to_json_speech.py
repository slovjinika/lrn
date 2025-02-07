import csv
import json

def tsv_to_json(tsv_file_path, json_file_path):
    """
    Конвертирует TSV файл с табами в JSON файл.  Правильно обрабатывает структуру данных.

    Args:
        tsv_file_path (str): Путь к TSV файлу.
        json_file_path (str): Путь к JSON файлу, который будет создан.
    """
    data = []
    with open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        header = next(reader)  # Читаем первую строку как заголовки

        for row in reader:
            row_dict = {}
            for i, col in enumerate(header):
                row_dict[col] = row[i]
            data.append(row_dict)

    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    tsv_file = 'input_2.tsv'  # Замените на ваш путь к TSV файлу
    json_file = 'output.json' # Замените на ваш путь к JSON файлу

    tsv_to_json(tsv_file, json_file)
    print(f"TSV файл '{tsv_file}' успешно конвертирован в JSON файл '{json_file}'")
