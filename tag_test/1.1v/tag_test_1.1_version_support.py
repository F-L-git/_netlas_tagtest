import netlas
import time
import csv
from requests.exceptions import RequestException

# API ключ
api_key = ''

# объект Netlas с API ключом
netlas_connection = netlas.Netlas(api_key=api_key)


def read_tags(file_path):
    with open(file_path, 'r') as file:
        tags = file.read().splitlines()
    return tags


def check_version_support(tag, retries=3, delay=1):
    query = f'tag.{tag}.version:<10000'
    for attempt in range(retries):
        try:
            netlas_query = netlas_connection.count(query=query)
            if 'count' in netlas_query and netlas_query['count'] > 0:
                return netlas_query['count'], f"Version supported, {netlas_query['count']} items found"
            else:
                return 0, "Version not supported"

        except netlas.exception.APIError as e:
            if 'Request limit' in str(e):
                time.sleep(delay)  # Задержка перед повторной попыткой
            elif 'ReadTimeout' in str(e):
                time.sleep(delay * 2)

    return 0, f"Error: Max retries exceeded for tag: {tag}"


# Чтение тегов из файла
tags = read_tags('tag_list/tag_list_part2.txt')

# Инициализация CSV файла и запись заголовка
with open('tag_version_support_results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Tag', 'Version Support', 'Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Проверка поддержки версий для каждого тега
    for index, tag in enumerate(tags, start=1):
        print(f"Checking version support for tag {index}/{len(tags)}: {tag}")

        # Проверка поддержки версионности
        num_version_results, version_message = check_version_support(tag)
        if num_version_results > 0:
            status = "Version Supported"
            print(
                f"[VERSION SUPPORTED] Tag: {tag}, Message: {version_message}")
        else:
            status = "Version Not Supported"
            print(
                f"[VERSION NOT SUPPORTED] Tag: {tag}, Message: {version_message}")

        # Запись результата в CSV файл
        writer.writerow(
            {'Tag': tag, 'Version Support': version_message, 'Status': status})

        print('-' * 50)  # Разделитель между проверками тегов
        time.sleep(1)  # Задержка между запросами

print("Version support results saved to tag_version_support_results.csv")
