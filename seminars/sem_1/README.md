# Семинар 1. Введение. Pandas

## Pandas

Основной материал по pandas находится в блокноте: `pandas_intro_nb.ipynb`.

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

* на Linux/Mac:

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
* `ipykernel` - ядро для работы ноутбуков (`.ipynb`)
* `jupyter`
* `matplotlib` - библиотека для построения графиков
* `seaborn` - еще библиотека для графиков

```bash
pip install pandas jupyter ipykernel matplotlib seaborn
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
Пока что достаточно `pandas`