import pandas as pd
import requests
import logging
import random

logging.basicConfig(filename='./test_service.log',level=logging.INFO)

print("Старт тестирования")
logging.info(f"Старт тестирования")

# задаём адрес сервиса рекомендаций и необходимые хедеры для запросов
service_url = 'http://127.0.0.1:8010'
headers = {
    'Content-type': 'application/json', 
    'Accept': 'text/plain'
    }

# подгружаем данные для тестирования
evenst = pd.read_parquet('events.parquet')
items = pd.read_parquet('items.parquet')

def map_response(resp):
    '''
    Обертка над ответом сервиса
    '''
    
    if resp.status_code == 200:
        recs = resp.json()
    else:
        recs = []
        print(f"status code: {resp.status_code}")
    
    return recs

def test_recs(recs, user_id):
    # берём 5 треков из рекомендованного набора
    print(recs['recs'])
    track_ids = random.sample(recs['recs'],k=5)
    for item in track_ids:
        # сохранем историю его взаимодействия с треком
        req = {
            'user_id' : user_id,
            'item_id' : item
        }   

        print(f"Пытаемся сохранить событие взаимодействия {user_id} и треком {item}")
        logging.info(f"Пытаемся сохранить событие взаимодействия {user_id} и треком {item}")
        logging.info(req)
        resp = requests.post(service_url + '/put', headers=headers, params=req)
        info = map_response(resp)

        print(f"Cобытие взаимодействия {user_id} и треком {item} сохранено с ответом {info}")
        logging.info(f"Cобытие взаимодействия {user_id} и треком {item} сохранено с ответом {info}")
        
        # после каждого нового события смотрим на состав рекомендаций
        req = {
            'user_id' : user_id,
            'k' : 10
        }
        print(f"Запрос рекомендаций для пользователя {user_id}")
        logging.info(f"Запрос рекомендаций для пользователя {user_id} {req}")

        resp = requests.post(service_url + '/recommendations', headers=headers, params=req)
        recs = map_response(resp)

        print(f"Получены рекомендации для пользователя {user_id}")
        logging.info(f"Получены рекомендации для пользователя {user_id}")
        logging.info(recs)

# выбираем пользователя
user_id = evenst['user_id'].sample(1).iloc[0]

print("Завершена подготовка данных")
logging.info(f"Завершена подготовка данных")

history = evenst[evenst['user_id']==user_id]['item_id'].sample(10)

logging.info(f"История пользователя {user_id} из 10 треков: ")
logging.info(history)

print(f"Запрос рекомендаций для пользователя {user_id}")
logging.info(f"Запрос рекомендаций для пользователя {user_id}")
req = {
    'user_id' : user_id,
    'k' : 10
}
logging.info(req)

resp = requests.post(service_url + '/recommendations', headers=headers, params=req)
recs = map_response(resp)

print(f"Получены рекомендации для пользователя {user_id}")
logging.info(f"Получены рекомендации для пользователя {user_id}")
logging.info(recs)

test_recs(recs, user_id)

print("Завершено тестирование на пользователе с историей")
logging.info(f"Завершено тестирование на пользователе с историей")


# выбираем "холодного" пользователя 
user_id = evenst['user_id'].max() + 1

print(f"Выбран холодный пользователь {user_id} для тестирования")
logging.info(f"Выбран холодный пользователь {user_id} для тестирования")

req = {
    'user_id' : user_id,
    'k' : 10
}
print(f"Запрос рекомендаций для пользователя {user_id}")
logging.info(f"Запрос рекомендаций для пользователя {user_id} {req}")

resp = requests.post(service_url + '/recommendations', headers=headers, params=req)
recs = map_response(resp)

print(f"Получены рекомендации для пользователя {user_id}")
logging.info(f"Получены рекомендации для пользователя {user_id}")
logging.info(recs)

test_recs(recs, user_id)

print("Тестирование завершено")