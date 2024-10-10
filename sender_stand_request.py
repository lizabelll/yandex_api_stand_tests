# Импортируем модуль configuration, который, мы создали выше - он содержит настройки подключения и путь к документации
from http.client import responses

import configuration

import requests

import data


# Определяем функцию get_docs, которая не принимает параметров
def get_docs():
    # Выполняем GET-запрос к URL, который складывается из базового URL-адреса сервиса
    # и пути к документации, заданных в модуле конфигурации
    # Функция возвращает объект ответа от сервера
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)

def get_logs():
    b = configuration.URL_SERVICE + configuration.LOG_MAIN_PATH
    params = {"count":20}
    return requests.get(b, params)

def get_users_table():
    return requests.get(configuration.URL_SERVICE+ configuration.USERS_TABLE_PATH)

# Определение функции post_new_user для отправки POST-запроса на создание нового пользователя
def post_new_user(body):

    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

# response = post_new_user(data.user_body)

def post_products_kits(products):
    url = configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH
    return requests.post(url = url, headers = data.headers, json = data.product_ids)

response = post_products_kits(data.product_ids)

