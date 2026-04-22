# Docker Compose

Для обеспечения воспроизводимости и изоляции компонентов проекта используется **Docker Compose**. Это позволяет развернуть все приложение одной командой

## Архитектура контейнеров

В проекте задействованы следующие компоненты:
* **PostgreSQL**: База данных для хранения метаинформации Airflow.
* **MinIO**: Объектное хранилище (S3-compatible), выступающее в роли Data Lake.
* **Airflow (Scheduler/Webserver)**: Система управления и запуска пайплайнов.
* **PySpark**: Контейнер с предустановленным Spark для обработки данных (для примера будет в контейнере с airflow).

## Подготовка и сборка

Если вы вносите изменения в конфигурации контейнеров (Dockerfile), необходимо пересобрать образы

Контейнеры можно создать на основе тех образов, которые уже есть на локальной машине или указать путь до соответствующих Dockerfile'ов. 
Также можно использовать образы с Docker Hub. 

Образы собираются и можно переиспользовать сколько угодно раз. 
Контейнеры - создаются и удаляются только на период использования.

Команда для запуска (в директории, где находится файл docker-compose.yml):
```bash
docker-compose up -d
```

Проверить, что контейнеры запущены:
```bash
docker ps
```

Выключить:
```bash
docker-compose down -v
```

**Все данные, которые были получены в результате работы приложения (результаты вычислений, кеш установок и прочее) будет удален после выключения.**
Контейнеры создаются только на время запуска. То есть, чтобы не потерять какую-то важную информацию - необходимо монтировать директории с хоста, чтобы сохранение осуществлялось в них (файлы баз данных, конфигурации, кеш установок и прочее).


В файле `docker-compose.yml` определяется конфигурация сервисов (компонентов приложения)
Пример
```docker-compose.yml
services:
  # База данных для метаданных Airflow
  postgres:
    image: psql_img:16
    # build: ./postgres # Если собирать с Dockerfile
    container_name: postgres_container
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5
```

Также можно монтировать директории, пробрасывать порты и другое.
```
    ports:
        - "8080:8080"
    volumes:
        - ./airflow/dags:/opt/airflow/dags
        - ./airflow/logs:/opt/airflow/logs
        - ./airflow/spark_local_cache:/opt/airflow/spark_local_cache
```


### Используемые образы

Образ хранилища MinIO (с Docker Hub) `./storage_lakehouse/Dockerfile` (собрался)

Образ airflow (скачан с Docker Hub) `./airflow/Dockerfile`

Образ postgres (нужен для хранения метаданных airflow, скачан с Docker Hub) `./postgres/Dockerfile` (собрался)


### Postgres
Проверить, что все работает

1) Собрать образ

cd /postgres

```cmd
docker build -t psql_img:16 .
```

```cmd
docker run -d ^
-e POSTGRES_USER=userairflow ^
-e POSTGRES_PASSWORD=pass1 ^
-e POSTGRES_DB=db ^
-p 5432:5432 ^
psql_img:16
```

Войти в контейнер (beautiful_hypatia - имя контейнера)
```cmd
docker exec -it beautiful_hypatia bash
```

Выполнить
```bash
psql -U userairflow -d db
```

Выйти из psql
```
\q
```

Остановить контейнер:
```cmd
docker stop container_name
```

### MinIO

Новый образ `./storage_lakehouse/Dockerfile`
Не собираем сами, а используем с docker hub

cd storage_lakehouse

```cmd
docker build -t storage:latest .
```

Создать контейнер
```cmd
docker run -d ^
  -p 9050:9000 ^
  -p 9051:9001 ^
  --env-file .env ^
  -v ./storage_data:/data ^
  --name minio-storage ^
  storage:latest ^
  server /data --console-address :9001
```

Зайти в контейнер
```cmd
docker exec -it minio-storage sh
```


## Запуск docker-compose

Чтобы собрать все контейнеры приложения:
1) Перейти в директорию с конфигурационным файлом `docker-compose.yml`
2) Запустить его
```cmd
docker compose up -d
```

3) Выключение 
```cmd
docker compose down 
```

Можно проверить, что все контейнеры работают, выполнив:
```cmd
docker ps
```

Также можно проверить, какие образы были созданы во время выполнения
```cmd
docker images
```