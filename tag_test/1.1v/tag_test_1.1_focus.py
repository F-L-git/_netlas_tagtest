import netlas
import time
import csv

# API ключ
api_key = 'mA3BPrqcOdh05mFDB9GVnkmVIXPW38Ua'

# объект Netlas с API ключом
netlas_connection = netlas.Netlas(api_key=api_key)


def read_tags(file_path):
    try:
        with open(file_path, 'r') as file:
            tags = file.read().splitlines()
        return tags
    except Exception as e:
        print(f"[ERROR] Failed to read tags from file {file_path}: {e}")
        return []


def search_by_tag(tag, retries=3, delay=1, version=None):
    if version:
        query = f'tag.{tag}.version:{version}'
    else:
        query = f'tag.name:{tag}'

    for attempt in range(retries):
        try:
            netlas_query = netlas_connection.count(query=query)
            if 'count' in netlas_query:
                total_results = netlas_query['count']
                return total_results, f"{total_results} items found"
            else:
                return 0, "No total_count in response"

        except netlas.exception.APIError as e:
            print(
                f"[API ERROR] Attempt {attempt + 1} for tag '{tag}' failed: {e}")
            if 'Request limit' in str(e):
                print('Request limit. Waiting a minute for a new attempt...')
                time.sleep(60)  # Подождать минуту перед повторной попыткой
        except Exception as e:
            print(
                f"[ERROR] Unexpected error during search for tag '{tag}': {e}")
        time.sleep(delay)  # Задержка перед повторной попыткой

    return 0, f"Error: Max retries exceeded for tag: {tag}"


def check_version_support(tag, retries=3, delay=1):
    query = f'tag.{tag}.version:<10000'
    for attempt in range(retries):
        try:
            netlas_query = netlas_connection.count(query=query)
            if 'count' in netlas_query and netlas_query['count'] > 0:
                total_results = netlas_query['count']
                return total_results, "Version supported"
            else:
                return 0, "Version not supported"

        except netlas.exception.APIError as e:
            print(
                f"[API ERROR] Attempt {attempt + 1} for version check of tag '{tag}' failed: {e}")
            if 'Request limit' in str(e):
                print('Request limit. Waiting a minute for a new attempt...')
                time.sleep(60)  # Задержка перед повторной попыткой
            elif 'ReadTimeout' in str(e):
                print('Read timeout. Waiting double the delay before a new attempt...')
                time.sleep(delay * 2)
        except Exception as e:
            print(
                f"[ERROR] Unexpected error during version check for tag '{tag}': {e}")
        time.sleep(delay)

    return 0, f"Error: Max retries exceeded for tag: {tag}"


# Чтение тегов из файла
tags = read_tags('tag_list/tag_list_part2.txt')

# Инициализация CSV файла и запись заголовка
with open('tag_test_results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Tag', 'Total Results',
                  'Version Support', 'Status', 'Message']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Проверка работы тегов без версий
    for index, tag in enumerate(tags, start=1):
        print(f"Checking tag {index}/{len(tags)}: {tag}")

        # Проверка работы тега без версии
        num_results, message = search_by_tag(tag)
        if num_results > 0:
            status = "Working"
            print(f"[WORKING] Tag: {tag}, Message: {message}")
        else:
            if "Error" in message:
                status = "Error"
                print(f"[ERROR] Tag: {tag}, Message: {message}")
            else:
                status = "Not Working"
                print(f"[NOT WORKING] Tag: {tag}, Message: {message}")

        # Проверка поддержки версионности (если версия поддерживается)
        if num_results > 0:
            num_version_results, version_message = check_version_support(tag)
            if num_version_results > 0:
                print(
                    f"[VERSION SUPPORT] Tag: {tag}, Message: {version_message}")
            else:
                print(
                    f"[NOT SUPPORTED] Tag: {tag}, Message: {version_message}")
        else:
            version_message = "Tag not supported"
            print(f"[NOT SUPPORTED] Tag: {tag}, Message: {version_message}")

        # Запись результата в CSV файл
        writer.writerow({'Tag': tag, 'Total Results': num_results,
                        'Version Support': version_message, 'Status': status, 'Message': message})

        print('-' * 50)  # Разделитель между проверками тегов
        time.sleep(1)  # Задержка между запросами

print("Test results saved to tag_test_results.csv")
