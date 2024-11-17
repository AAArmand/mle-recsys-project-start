# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/yandex-praktikum/mle-project-sprint-4-v001.git
```

## Активируйте виртуальное окружение

Используйте то же самое виртуальное окружение, что и созданное для работы с уроками. Если его не существует, то его следует создать.

Создать новое виртуальное окружение можно командой:

```
python3 -m venv .venv_recsys_project
```

После его инициализации следующей командой

```
source .venv_recsys_project/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными:
- [tracks.parquet](https://storage.yandexcloud.net/mle-data/ym/tracks.parquet)
- [catalog_names.parquet](https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet)
- [interactions.parquet](https://storage.yandexcloud.net/mle-data/ym/interactions.parquet)
 
Скачайте их в директорию локального репозитория. Для удобства вы можете воспользоваться командой wget:

```
wget https://storage.yandexcloud.net/mle-data/ym/tracks.parquet

wget https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet

wget https://storage.yandexcloud.net/mle-data/ym/interactions.parquet
```

## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код для выполнения первой части проекта находится в файле `recommendations.ipynb`. Изначально, это шаблон. Используйте его для выполнения первой части проекта.

# Сервис рекомендаций

Код сервиса рекомендаций находится в файле `recommendations_service.py`.

Чтобы запустить необходимо выполнить:
```
uvicorn recommendations_service:app --port 8010
```

# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `test_service.py`.

Чтобы запустить необходимо выполнить:
```
python -m test_service
```

# Стратегия смешивания онлайн- и офлайн- рекомендаций

Поскольку мы не знаем, как пользователи отрегаируют на рекомендательную систему впервые, решил рандомно смешивать рекомендации  
После запуска рекомендательной системы или A/B тестов мы поймем и замерим общий NPS  
Далее сравним его с тем, что было до и будем делать выводы  
Также можно проанализировать показатели активности и прочие важные нам продуктовые метрики  
Относительно выводов после запуска можно будет изменить стратегию смешивания на более сложную