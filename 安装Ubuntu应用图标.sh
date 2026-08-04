#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$HOME/.local/share/nono-desktop-pet"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/nono-desktop-pet.desktop"

if ! command -v python3 >/dev/null 2>&1; then
    echo "未找到 Python 3，请先安装：sudo apt install python3"
    exit 1
fi

if ! python3 -c "import PyQt5" >/dev/null 2>&1; then
    echo "未找到 Linux 透明窗口组件，请先安装："
    echo "sudo apt update && sudo apt install python3-pyqt5"
    exit 1
fi

mkdir -p "$APP_DIR" "$DESKTOP_DIR"
cp "$PROJECT_DIR/nono_linux.py" "$APP_DIR/nono_linux.py"
rm -rf "$APP_DIR/assets"
cp -R "$PROJECT_DIR/assets" "$APP_DIR/assets"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=嫑嫑 nono
Comment=一只住在桌面上的小锅
Exec=env QT_QPA_PLATFORM=xcb python3 $APP_DIR/nono_linux.py
Icon=$APP_DIR/assets/idle.png
Terminal=false
Type=Application
Categories=Utility;
StartupNotify=false
EOF

chmod +x "$DESKTOP_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi

echo "安装完成！现在可以在 Ubuntu 应用菜单中搜索“嫑嫑 nono”启动。"
