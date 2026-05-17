import netlas

# API ключ
api_key = 'YOUR_API_KEY'

# объект Netlas с вашим API ключом
netlas_connection = netlas.Netlas(api_key=api_key)

# Список тегов и запросов для проверки
queries = [
    'tag.name:nginx',
    'tag.nginx:*',
    'tag.category:webmail',
    'tag.woocommerce.version:<5',
    'tag.vbulletin.version:>=4 AND tag.vbulletin.version:<5',
    # другие запросы здесь
]

# Функция для выполнения запросов и вывода результатов


def search_by_query(query):
    try:
        print(f"Searching for: {query}")
        netlas_query = netlas_connection.query(query=query)
        for response in netlas_query['items']:
            print(
                f"{response['data']['ip']}:{response['data']['port']}{response['data']['path']} [{response['data']['protocol']}]")
    except Exception as e:
        print(f"An error occurred while searching for {query}: {e}")


# запросы для всех тегов и запросов
for query in queries:
    search_by_query(query)
