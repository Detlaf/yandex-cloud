**Оцифровщик документов**

Программа получает на вход путь к директории с изображениями и pdf файлами, 
а также путь к файлу с OAuth токеном.
Производится поочередная обработка изображений и pdf файлов в указанной директории
и во всех вложенных, извлеченный из каждого файла текст записывается в итоговый 
текстовый файл.

**Запуск**: `python digit_docs.py --image-dir= --oauth-path=`

**Загрузка файлов в Object Storage**

Приложение на Flask, которое отображает список файлов, находящихся в Object Storage, и загружает в него файлы.
Для работы нужно в файле .aws/credentials указать данные секретного ключа.

**Запуск**: `python flask_object_storage.py`<br>
Главная страница:<br>
`127.0.0.1:5000`<br>
Страница для загрузки документов:<br>
`127.0.0.1:5000/storage`
 
