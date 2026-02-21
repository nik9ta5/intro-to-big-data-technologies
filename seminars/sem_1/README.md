# Семинар 1. Введение. Pandas

Содержание:
* [Pandas](#pandas)
* [PySpark](#pyspark)
* [Подготовка среды для работы](#подготовка-среды-для-работы)
    - [Установка виртуального окружения](#установка-виртуального-окружения-venv)
    - [Как запустить блокнот в VS Code](#как-запустить-блокнот-в-vs-code)
* [Как установить PySpark](#как-установить-pyspark)


## Pandas

Основной материал по pandas находится в блокноте: [`./pandas_intro_nb.ipynb`](./pandas_intro_nb.ipynb).

## PySpark

Основной материал по pandas находится в блокноте: [`./pyspark_intro_nb_2.ipynb`](./pyspark_intro_nb_2.ipynb).

### HW 1

Дополнительный материал по PySpark и первое задание в блокноте: [`./pyspark_taxi_simple_eda.ipynb`](./pyspark_taxi_simple_eda.ipynb)

---
## Подготовка среды для работы

1. Для работы с блокнотами (`.ipynb`) можно использовать [Google Colab](https://colab.google/)

Подключить Google Drive, загрузить файл на Google Drive и использовать файл в блокноте.

```python
from google.colab import drive
drive.mount('/content/drive')
```

Или использовать интерфейс

2. Для локальной работы с блокнотами: установить любую IDE + Python.


### Установка виртуального окружения (venv)

1. Перейти куда хотим установить виртуальное окружение

```bash
cd dir_name
python -m venv venv
```

2. Для активации виртуального окружения: 
* на Windows:

```cmd
.\venv\Scripts\activate
```

* на Linux/macOS:

```bash
source ./venv/bin/activate
```

Для выключения: 

```bash
deactivate
```

3. После активации окружения можно посмотреть установленные пакеты:

```bash
# или pip freeze
pip list
```

Установить необходимые библиотеки:
* `pandas`
* `pyspark`
* `ipykernel` - ядро для работы ноутбуков (`.ipynb`)
* `jupyter`
* `matplotlib` - библиотека для построения графиков
* `seaborn` - еще библиотека для графиков

```bash
pip install pandas jupyter ipykernel matplotlib seaborn pyspark==3.5.3
```

### Как запустить блокнот в VS Code

1. Открываем директорию в которой находится папка с виртуальным окружением

2. Создаем блокнот (файл с расширением `.ipynb`)

3. Выбрать `Select Kernel` - `Select Another Kernel` ("Выбрать другое ядро") - `Python Environment` - выбрать созданное окружение (`venv`)
Если в выпадающем списке окружения нет — перезапустите VS Code.

Импортировать pandas в блокнот

```python
import pandas as pd
```

Запускать ячейки (CTRL + ENTER)

Все, блокнот работает в созданном окружении 

---
Пока что достаточно `pandas`, `pyspark`

## Как установить PySpark

Для работы PySpark необходимо установить JAVA (JDK 17 или JDK 21 (рекомендуется 21))
Ссылка на JDK 21: https://www.oracle.com/java/technologies/javase/jdk21-archive-downloads.html
Или: https://jdk.java.net/21/

1. Установить JAVA через скаченный установочник (или распаковать скачанный архив). `Важно: запомнить путь установки`.
2. Добавить путь к JAVA в системные переменные.
    2.1) на Windows:
    "Изменение системных переменных среды" - "Переменные среды" - Раздел "Системные переменные" - "Создать" (Имя переменной: **JAVA_HOME**, Значение: `путь до установленной JAVA`) - Переменная **Path** - "Изменить" - "Создать" (`%JAVA_HOME%\bin`) - ОК - ОК - ОК
    
    Проверить что Java видна: 
    ```cmd
    java --version
    ```

    2.2) на Linux: (в своем семействе Linux использовать свою систему управления пакетами: apk или apt)
    Ubuntu/Debian:
    ```bash
    sudo apt update
    sudo apt install openjdk-21-jdk

    java -version
    javac -version
    ```

    Alpine Linux:
    ```sh
    apk add openjdk21
    java -version
    javac -version
    ```
    2.3) macOS:
    Установка:
    ```bash
    brew install openjdk@21
    ``` 
    Проверить наличие java:
    ```bash
    java -version
    ```
3. Установить PySpark
```
pip install pyspark==3.5.3
```
macOS/Linux:
```bash
pip3 install pyspark==3.5.3
```
Или более новую версию