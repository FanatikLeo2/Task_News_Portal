# Task_News_Portal
* Подключен брокер Redis.
+ Установлен Celery.
* Создан файл celery.py, добавлен код.
+ Добавлен код в __init__.py.
* Добавлены настройки Celery и адрес брокера Redis в settings.py.
+ Добавлены таски в tasks.py и реализовано асинхронное выполнение этих задач:
+ send_notifications - рассылка писем подписчикам при добавлении новости 
+ send_last_week_news - еженедельная рассылка подписчикам с последними новостями (каждый понедельник в 8:00 утра)
* команда для запуска Celery:
* celery -A NewsPortal worker -l info -P threads --concurrency 4
+ команда для запуска периодических задач:
+ celery -A NewsPortal beat -l INFO