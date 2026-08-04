#!/usr/bin/env bash

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
    echo "未找到 Python 3，请先安装：sudo apt install python3"
    exit 1
fi

if ! python3 -c "import tkinter" >/dev/null 2>&1; then
    echo "未找到 Tkinter，请先安装：sudo apt install python3-tk"
    exit 1
fi

python3 nono.py
