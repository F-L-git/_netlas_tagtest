import netlas
import csv
import time
from requests.exceptions import RequestException

# API ключ
api_key = 'mA3BPrqcOdh05mFDB9GVnkmVIXPW38Ua'

# объект Netlas с API ключом
netlas_connection = netlas.Netlas(api_key=api_key)


def read_tags(file_path):
    with open(file_path, 'r') as file:
        tags = file.read().splitlines()
    return tags


def search_by_tag(tag, retries=3, delay=1, version=None):
    if version:
        query = f'tag.{tag}.version:{version}'
    else:
        query = f'tag.name:{tag}'

    for attempt in range(retries):
        try:
            netlas_query = netlas_connection.query(query=query)
            if 'items' in netlas_query and netlas_query['items']:
                total_results = netlas_query.get('total', 0)
                return True, f"{total_results} results found"
            else:
                return False, "No results found"
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed for tag: {tag}. Error: {e}")
        time.sleep(delay)  # Задержка перед повторной попыткой
    return False, f"Error: Max retries exceeded for tag: {tag}"


def check_version_support(tag, retries=3, delay=1):
    query = f'tag.{tag}.version:<100'
    for attempt in range(retries):
        try:
            netlas_query = netlas_connection.query(query=query)
            if 'items' in netlas_query and netlas_query['items']:
                return True, "Version supported"
            else:
                return False, "Version not supported"
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed for tag: {tag}. Error: {e}")
        time.sleep(delay)  # Задержка перед повторной попыткой
    return False, f"Error: Max retries exceeded for tag: {tag}"


# Чтение тегов из файла
tags = read_tags('tag_list/tag_list_part2.txt')

# Инициализация CSV файла и запись заголовка
with open('tag_test_results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Tag', 'Version Support', 'Status', 'Message']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Проверка работы тегов без версий и поддержка версионности
    for index, tag in enumerate(tags, start=1):
        print(f"Checking tag {index}/{len(tags)}: {tag}")

        # Проверка поддержки версионности
        version_supported, version_message = check_version_support(tag)

        if version_supported:
            # Проверка работы тега без версии
            is_working, message = search_by_tag(tag)
            if is_working:
                status = "Working"
                print(f"[WORKING] Tag: {tag}, Message: {message}")
            else:
                if "Error" in message:
                    status = "Error"
                    print(f"[ERROR] Tag: {tag}, Message: {message}")
                else:
                    status = "Not Working"
                    print(f"[NOT WORKING] Tag: {tag}, Message: {message}")

            # Запись результата в CSV файл
            writer.writerow({'Tag': tag, 'Version Support': version_message,
                            'Status': status, 'Message': message})
        else:
            print(f"[NOT SUPPORTED] Tag: {tag}, Message: {version_message}")
            writer.writerow({'Tag': tag, 'Version Support': version_message,
                            'Status': "Not Supported", 'Message': version_message})

        print('-' * 50)  # Разделитель между проверками тегов
        time.sleep(1)  # Задержка между запросами

print("Test results saved to tag_test_results.csv")
