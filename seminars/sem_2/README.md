# Семинар 2. Введение в Docker и MinIO

Содержание:
* [Docker](#docker)
    - [Команды](#команды-которые-могут-потребоваться)
    - [Создание Dockerfile](#создание-dockerfile)
    - [Монтирование директорий](#монтирование-директорий)
    - [Проброс портов](#проброс-портов)
    - [Установка переменных среды](#установка-переменных-среды)
* [MinIO](#minio)
* [Подключение PySpark к MinIO](#подключение-pyspark-к-minio)
* [HW 2](#hw-2)


## Docker
Скачать Docker Desktop
Для подробного ознакомления есть официальная документация [документация](https://docs.docker.com/get-started/)

[What is Docker?](https://docs.docker.com/get-started/docker-overview/)
[Как создавать Dockerfile](https://docs.docker.com/reference/dockerfile)

Потрясающее объяснение с курса Data Engineering про [Docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/docker-sql)


### Команды, которые могут потребоваться

Данный список неполный, но наиболее частые команды, которые потребуются в рамках курса

##### Узнать установленную версию docker
```bash
docker --version # версия docker
```

##### Показать существующие образы (images)
```bash
docker images
```

##### Показать запущенные контейнеры
```bash
docker ps
```

##### Показать все контейнеры
```bash
docker ps -a
```

##### Создать образ
```bash
docker build -t name:tag_0_1 . # Создать образ на основе Dockerfile
```
**Точка в конце указывает на текущую директорию**, если требуемый Dockerfile находится в другой директории, указать соответствующий путь

##### Создать контейнер
```bash
docker run -it name:tag_0_1
```
Для выхода из контейнера:
```bash
exit
```

##### Для запуска контейнера
```bash
docker start -i CONTAINER_ID
```

##### Удалить контейнер по ID
```bash
docker rm CONTAINER_ID
```

##### Удалить образ по ID
```bash
docker rmi IMAGE_ID
```

##### Удалить все контейнеры 
```bash
docker container prune
```

##### Сколько докер занимает места
```
docker system df
```

##### Посмотреть историю слоев образа
```bash
docker history image_name
```


### Создание Dockerfile
Описывает последовательность действий, необходимых для создания образа

Указываем базовый образ, который будет использоваться

```Dockerfile
FROM alpine:latest # Базовый образ, который используется при создании контейнера

WORKDIR /app # Установить рабочую директорию

COPY index.py index.py # копирование файла (первое название - имя файла, второе - имя файла в контейнере)

RUN apk add --no-cache wget # Выполнить команду

CMD ["sh"] # Команды, которые будут выполнены после запуска контейнера
```

Скачивание minIO при создании образа

```Dockerfile
RUN apk add --no-cache wget &&\
    wget https://dl.min.io/server/minio/release/linux-amd64/minio &&\
    chmod +x minio &&\
    mv minio /usr/local/bin &&\
    mkdir -p /data
```

Если хотим копировать всю директорию
```Dockerfile
COPY . .
```

### Монтирование директорий
Монтирование директории с хоста, при создании контейнера
```bash
docker run -it -v /path/2/pc:/path/2/container image_name:tag
```
При создании контейнера, есть возможность указать директорию на локальной машине, к которой можно будет получить доступ из контейнера. 

Например, директория на вашем ПК: `/path/2/pc/`, будет отображаться в контейнере по пути: `/path/2/container/`.
Следовательно, файлы, которые будут создаваться в контейнере, будут отображаться на вашем ПК, даже после выключения контейнера. 

Можно монтировать директорию с проектом, во время разработки, чтобы не пересобирать образ каждый раз. 
Можно монтировать директорию для создания временных файлов, файлов БД, если хотите не потерять файлы после удаления контейнера.

**(Для более корректного объяснения монтирования директорий рекомендую ознакомиться с соответствующей документацией)**.

### Проброс портов
```bash
docker run -it -p 9000:9000 -p 9001:9001 image_name:tag
```
Первое значение - порт на локальной машине, второе - порт в контейнере

### Установка переменных среды
```bash
docker run -it -e "MINIO_ROOT_USER=root_name" image_name:tag
```
Флаг `-e` позволяет установить переменную среды, вместо вызова `export` внутри контейнера.


Примерная команда для создания контейнера
```bash
docker run -it \
    -p 9000:9000 \
    -e "MINIO_ROOT_USER=root_name" \
    -v ./data:/data \
    image_name:tag
```


## MinIO
Объектное хранилище

(aistore - enterprise версия, для данного курса не требуется)

Файлы для скачивания, для соответствующей ОС и пр: https://dl.min.io/server/minio/release/

Достаточно скачать: https://dl.min.io/server/minio/release/linux-amd64/minio

Для скачивания использовать утилиту wget
```bash
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio # установить права для запуска
mv minio /usr/local/bin # переместить в /usr/local/bin
mkdir -p /data # создать директорию, в которой будут располагаться бакеты и пр.
```

Перед запуском необходимо установить следующие переменные:
```bash
export MINIO_BROWSER=on
export MINIO_IDENTITY_OPENID_ENABLE=off
export MINIO_CALLHOME_ENABLE=off
```

И необходимо установить имя и пароль для root (вопросы безопасности в рамках данного задания опущены)
```bash
export MINIO_ROOT_USER=root_name
export MINIO_ROOT_PASSWORD=root_password
```

Проверить что система видит minio
```bash
minio --version
```

Для запуска:
```bash
minio server /data --console-address :9001
```

Для работы, при создании контейнера должны быть прокинуты порты (9000 и 9001)
Далее, для взаимодействия с хранилищем по API, можно использовать соответствующий путь (будет примерно: http://127.0.0.1:9000)
Для взаимодействия через WebUI, через браузер (примерный адрес: http://127.0.0.1:9001)

Для загрузки файлов, предлагается использовать WebUI.
Перейти по соответствующему пути (http://127.0.0.1:9001)
Зайти под root, использовать указанные имя и пароль.
Создать бакет и загрузить файлы.


## Подключение PySpark к MinIO

---
**Для Windows**
(Для другой ОС - перейти к [Настройка конфигурации SparkSession в PySpark](#настройка-конфигурации-sparksession-в-pyspark))

Перейти в репозиторий: https://github.com/cdarlint/winutils/tree/master/hadoop-3.3.6/bin 

И скачать 2 файла: `hadoop.dll` и `winutils`. Затем в `C:\` создать папку с именем `hadoop`, в ней `bin` (должно получиться `C:\hadoop\bin`) и перенести скачанные файлы.

Изменение системных переменных - Переменные среды - Системные переменные - Создать (`HADOOP_HOME`, указать путь `C:\hadoop`).
Добавить в Path - изменить - `%HADOOP_HOME%\bin` - Ок - Ок - Ок.

---

### Настройка конфигурации SparkSession в PySpark

```python
spark = (
    SparkSession.builder 
    .appName("MinIO test")
    .master("local[*]")  
    .config("spark.jars.packages", 
        "org.apache.hadoop:hadoop-aws:3.3.4,"
        "com.amazonaws:aws-java-sdk-bundle:1.12.262") 
    # адрес для подключения
    .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000") 
    # ключи доступа
    .config("spark.hadoop.fs.s3a.access.key", "root_name") 
    .config("spark.hadoop.fs.s3a.secret.key", "root_password") 

    .config("spark.hadoop.fs.s3a.path.style.access", "true") 
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") 
    # Для локальной работы отключаем SSL, для реальных проектов обязательно указывать true.
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") 
    .getOrCreate()
)
```

Установка
```python
.config("spark.jars.packages", 
        "org.apache.hadoop:hadoop-aws:3.3.4,"
        "com.amazonaws:aws-java-sdk-bundle:1.12.262")
```
скачает файлы, требующиеся для подключения к хранилищам типа S3 (в нашем примере MinIO).

Установка 
```python
.config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000") 
.config("spark.hadoop.fs.s3a.access.key", "root_name") 
.config("spark.hadoop.fs.s3a.secret.key", "root_password") 
```
настраивает соответствующий endpoint для подключения к хранилищу, имя root и пароль root.

### Создание датафрейма к источнику данных

Для создания датафрейма к источнику данных (хранилищу MinIO).

В данном примере `taxi-bucket` - название бакета с файлами.

`*.parquet` - указывает, что все файлы с расширением .parquet (в одном бакете могут располагаться файлы только с одинаковым расширением).

```python
df = spark.read.parquet("s3a://taxi-bucket/*.parquet")
```

Все необходимые шаги были выполнены, теперь можно взаимодействовать с хранилищем через PySpark.


---
## HW 2:
1) Установить Docker Desktop
2) Скачать файлы за любые 2 месяца (`High Volume For-Hire Vehicle Trip Records`, можно взять файл с предыдушего задания): https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page 
3) Создать Docker image (образ) c MinIO 
    - *Важно:* Не копируйте датасеты в образ через `COPY`, образ станет слишком тяжелым.
4) Создать контейнер на основе созданного образа 
    - Пробросить порты 9000 и 9001
    - Задать переменные окружения для имени и пароля root
    - Смонтировать локальную папку для данных: `-v ./data:/data`
    *Совет*: Если используете монтирование, создайте папку с именем будущего бакета (например, `taxi-data`) внутри `./data` до запуска контейнера и положите файлы туда. Тогда MinIO сразу увидит бакет. Либо загрузите файлы через WebUI после запуска.
5) Загрузить файлы в хранилище. Убедитесь, что файлы загружены через WebUI
6) PySpark и анализ
    - Настроить подключение PySpark к MinIO.
    - Создать датафрейм к источнику данных.
    - Определить количество строк в датафрейме.
    - Определите за какие месяцы присутствуют записи, посчитайте записи за каждый месяц.
    - Определите среднее время поездки в минутах для каждого месяца.