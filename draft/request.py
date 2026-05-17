from netlas import Netlas

# Установите ваш API ключ
api_key = 'mA3BPrqcOdh05mFDB9GVnkmVIXPW38Ua'

# Создайте объект Netlas с вашим API ключом
netlas = Netlas(api_key)

# Укажите теги для поиска
tags = ['tag1', 'tag2', 'tag3']

# Выполните поиск с использованием тегов
results = netlas.search(query='', tags=tags)

# Выведите результаты
for result in results['data']:
    print(result)
