#!/bin/bash

# Имя папки виртуального окружения
VENV_DIR="venv"

# Проверка установлен ли python3-venv
if ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "Устанавливаем python3-venv..."
    apt-get update && apt-get install -y python3-venv
fi

# Создание виртуального окружения, если его нет
if [ ! -d "$VENV_DIR" ]; then
    echo "Создаем виртуальное окружение..."
    python3 -m venv $VENV_DIR
fi

# Активация и установка зависимостей
echo "Проверка зависимостей..."
./$VENV_DIR/bin/pip install -r requirements.txt -q

# Запуск скрипта
echo "Запуск сканера..."
./$VENV_DIR/bin/python3 check.py
