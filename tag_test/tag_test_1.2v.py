import netlas
import time
import csv

# API ключ
api_key = ''

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


def execute_with_retries(func, *args, retries=3, delay=1, **kwargs):
    for attempt in range(retries):
        time.sleep(delay)
        try:
            return func(*args, **kwargs)
        except netlas.exception.APIError as e:
            print(f"[API ERROR] Attempt {attempt + 1} failed: {e}")
            if 'Request limit' in str(e):
                print('Request limit. Waiting double the delay before a new attempt...')
                # Подождать двойное время перед повторной попыткой
                time.sleep(delay * 2)
            elif 'ReadTimeout' in str(e):
                print('Read timeout. Waiting double the delay before a new attempt...')
                time.sleep(delay * 2)
            else:
                print(
                    f"API error occurred: {e}. Waiting before next attempt...")
                time.sleep(delay)  # Задержка перед следующей попыткой
        except Exception as e:
            print(
                f"[ERROR] Unexpected error: {e}. Waiting before next attempt...")
            time.sleep(delay)
    print(f"[ERROR] Max retries exceeded for function {func.__name__}")
    return None


def search_by_tag(tag, version=None):
    if version:
        query = f'tag.{tag}.version:{version}'
    else:
        query = f'tag.name:{tag}'
    netlas_query = netlas_connection.count(query=query)
    if 'count' in netlas_query:
        total_results = netlas_query['count']
        return total_results, f"{total_results} items found"
    else:
        return 0, "No total_count in response"


def check_version_support(tag):
    query = f'tag.{tag}.version:<10000'
    netlas_query = netlas_connection.count(query=query)
    if 'count' in netlas_query and netlas_query['count'] > 0:
        total_results = netlas_query['count']
        return total_results, "Version supported"
    else:
        return 0, "Version not supported"


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
    result = execute_with_retries(search_by_tag, tag)
    if result:
        num_results, message = result
        if num_results > 0:
            status = "Working"
            print(f"[WORKING] Tag: {tag}, Message: {message}")
        else:
            status = "Not Working"
            print(f"[NOT WORKING] Tag: {tag}, Message: {message}")
    else:
        num_results, message, status = 0, "Error: Max retries exceeded", "Error"
        print(f"[ERROR] Tag: {tag}, Message: {message}")

    # Проверка поддержки версионности (если версия поддерживается)
    if num_results > 0:
        version_result = execute_with_retries(check_version_support, tag)
        if version_result:
            num_version_results, version_message = version_result
            if num_version_results > 0:
                print(
                    f"[VERSION SUPPORT] Tag: {tag}, Message: {version_message}")
            else:
                print(
                    f"[NOT SUPPORTED] Tag: {tag}, Message: {version_message}")
        else:
            version_message = "Error: Max retries exceeded"
            print(f"[ERROR] Tag: {tag}, Message: {version_message}")
    else:
        version_message = "Tag not supported"
        print(f"[NOT SUPPORTED] Tag: {tag}, Message: {version_message}")

    # Запись результата в CSV файл
    with open('tag_test_results.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Tag': tag, 'Total Results': num_results,
                         'Version Support': version_message, 'Status': status, 'Message': message})

    print('-' * 50)  # Разделитель между проверками тегов
    time.sleep(1)  # Задержка между запросами

print("Test results saved to tag_test_results.csv")
