import netlas

# API ключ
api_key = 'YOUR_API_KEY'

# объект Netlas с API ключом
netlas_connection = netlas.Netlas(api_key=api_key)

# Список категорий тегов для проверки
tag_categories = [
    'Maps', 'Marketing automation', 'Media servers', 'Message boards',
    'Miscellaneous', 'Mobile frameworks', 'Network', 'Network devices',
    'Network storage', 'Operating systems', 'PaaS', 'Page builders',
    'Payment processors', 'Photo galleries', 'Printers', 'Programming languages',
    'Remote access', 'Reverse proxies', 'Rich text editors', 'Router', 'SEO',
    'SSH server', 'SaaS', 'Search engines', 'Security', 'Social logins',
    'Static site generator', 'Tag managers', 'Telecom', 'UI frameworks',
    'Video players', 'VoIP', 'Web cameras', 'Web frameworks',
    'Web server extensions', 'Web servers', 'Webmail', 'Widgets', 'Wikis'
]

# Функция для выполнения запросов и вывода результатов


def search_by_tag_category(category):
    query = f'tag.category:"{category}"'
    try:
        print(f"Searching for: {query}")
        netlas_query = netlas_connection.query(query=query)
        for response in netlas_query['items']:
            print(
                f"{response['data']['ip']}:{response['data']['port']}{response['data']['path']} [{response['data']['protocol']}]")
    except Exception as e:
        print(f"An error occurred while searching for {query}: {e}")


# Запросы для всех категорий тегов
for category in tag_categories:
    search_by_tag_category(category)
