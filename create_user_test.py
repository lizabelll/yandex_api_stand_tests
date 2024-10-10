from wsgiref.validate import assert_

import data
import sender_stand_request
from data import user_body
from sender_stand_request import response


# эта функция меняет значения в параметре firstName
def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body


def positive_assert(first_name):
    # В переменную user_body сохраняется обновленное тело запроса с именем "Аа"
    user_body = get_user_body(first_name)
    #print("user_body: ", user_body)
    # В переменную user_response сохраняется результат запроса на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)
    #print("user_response.json(): ", user_response.json())
    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
           + user_body["address"] + ",,," + user_response.json()["authToken"]
    #print(str_user)
    assert users_table_response.text.count(str_user) == 1
#return users_table_response
    # print(users_table_response)
    return users_table_response

#Задание 1
def test_create_user_2_letter_in_first_name_get_success_response():
    return positive_assert("Aa")
a = test_create_user_2_letter_in_first_name_get_success_response()
print("тест 1", a)

#Задание 2
def test_create_user_15_letter_in_first_name_get_success_response():
    return positive_assert("Ааааааааааааааа")
b = test_create_user_15_letter_in_first_name_get_success_response()
print("тест 2", b)

#Задание 3
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
    "Имя может содержать только русские или латинские буквы, " \
    "длина должна быть не менее 2 и не более 15 символов"
    return response

def test_create_user_1_letter_in_first_name_get_error_response():
    return negative_assert_symbol("А")
c = test_create_user_1_letter_in_first_name_get_error_response()
print("тест 3", c)

#Задание 4
def test_create_user_16_letter_in_first_name_get_error_response():
    return negative_assert_symbol("Аааааааааааааааа")
print("тест 4", test_create_user_16_letter_in_first_name_get_error_response())

#Задание 5
def test_create_user_english_letter_in_first_name_get_success_response():
    return positive_assert("QWErty")
print ("тест 5", test_create_user_english_letter_in_first_name_get_success_response())

# Задание 6
def test_create_user_russian_letter_in_first_name_get_success_response():
    return positive_assert("Мария")
print ("тест 6", test_create_user_russian_letter_in_first_name_get_success_response())

# Задание 7
def test_create_user_has_space_in_first_name_get_error_response():
    return negative_assert_symbol ("Человек и Ко")
#print ("тест 7", test_create_user_has_space_in_first_name_get_error_response())

# Задание 8
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    return negative_assert_symbol("№%@")
print ("тест 8", test_create_user_has_special_symbol_in_first_name_get_error_response())

# Задание 9
def test_create_user_has_number_in_first_name_get_error_response():
    return negative_assert_symbol("123")
print ("тест 9", test_create_user_has_number_in_first_name_get_error_response())

# Задание 10
def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"
    return response

def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    return negative_assert_no_first_name(user_body)
print ("тест 10", test_create_user_no_first_name_get_error_response())
# Задание 11
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    return negative_assert_no_first_name(user_body)
print("тест 11", test_create_user_empty_first_name_get_error_response())

# Задание 12
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 500
    return response
print("тест 12", test_create_user_number_type_first_name_get_error_response())

