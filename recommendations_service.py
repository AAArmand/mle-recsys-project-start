import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from recsys_handler import RecSysHeandler
from events_store import EventStore
import random

rec_store = RecSysHeandler()
events_store = EventStore()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    logging.info("Starting")
    yield
    # этот код выполнится только один раз при остановке сервиса
    rec_store.stats()
    logging.info("Stopping")
    
# создаём приложение FastAPI
app = FastAPI(title="recommendations", lifespan=lifespan)

@app.post("/recommendations")
async def recommendations(user_id: int, k: int = 100):
    """
    Возвращает список рекомендаций длиной k для пользователя user_id
    """
    # вернёт k * 2 персональных рекомендаций если они подготовлены offline или k популярных треков
    # тут и ниже k умножаем на 2, чтобы было, что отсекать при необходимости и не ходить дополнитель за рекомендациями
    personal = rec_store.personal_rec(user_id, k*2)
    events = events_store.get(user_id, k)
    if len(events) == 0:
        # отдаём рекомендации для пользователя без истории
        recs = personal[:k]
    else:
        # для пользователей с историей запрашивем похожие треки
        recs_online = []
        for item_id in events:
            recs_online += rec_store.items_rec(item_id, k*2) 
        # убираем из рекомендаций треки, которые пользователь слушал и дубли от персональных/популярных
        recs_online = list(set(recs_online) - set(events) - set(personal))
        
        # ранжируем между собой случайным образом
        all_recs_for_rank = recs_online + personal
        
        recs = random.sample(all_recs_for_rank, k=k)

    return {"recs": recs}

@app.post("/put")
async def put(user_id: int, item_id: int):
    """
    Сохраняет событие для user_id, item_id
    """

    events_store.put(user_id, item_id)

    return {"result": "ok"}