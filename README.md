Как этим пользоваться:
1. Склонировать репозиторий. 
```bash
git clone git@github.com:milssky/generator_shpor.git
```
2. Создать виртуальное окружение.
```bash
python -m venv venv
```
или для macOS или Linux
```bash
python3 -m venv venv
```
3. Активировать окружение.
```bash
. .\venv\Scripts\activate
```
4. Установить необходимые для работы пакеты.
```bash
pip install -r requirements.txt
```
5. Положить zip-архивы шпаргалок, экспортированных из Notion в формате HTML, в директорию `zip`. Если директория будет пустая, скрипт сгенерирует папку `result` со служебной статикой. 
6. Запустить скрипт
```bash
python main.py
```
7. В результате работы будет создана папка result со всеми отформатированным шпаргалками и служебной статикой.


