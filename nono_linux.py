import random
import sys
from pathlib import Path

from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QWidget


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSET_NAMES = (
    "idle",
    "happy",
    "surprised",
    "zoom",
    "tired",
    "curious",
    "box",
    "nervous",
    "lotus",
    "wave",
    "tilted",
    "measure",
    "pout",
)


class NonoPet(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("嫑嫑 nono")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(280, 280)

        self.images = {
            name: QPixmap(str(ASSETS / f"{name}.png")) for name in ASSET_NAMES
        }
        missing = [name for name, image in self.images.items() if image.isNull()]
        if missing:
            raise FileNotFoundError("缺少素材：" + ", ".join(missing))

        self.state = "idle"
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 280, 280)
        self.image_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(self.images[self.state])

        self.tip = QLabel(self)
        self.tip.setStyleSheet(
            "background: #fff7d6; color: #332f3a; border-radius: 8px;"
            "padding: 6px 10px; font-size: 14px;"
        )
        self.tip.setAlignment(Qt.AlignCenter)
        self.tip.hide()

        self.drag_start = QPoint()
        self.window_start = QPoint()
        self.dragged = False
        self.system_move_started = False
        self.setCursor(QCursor(Qt.PointingHandCursor))

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.right() - 310, screen.bottom() - 330)

        self.idle_timer = QTimer(self)
        self.idle_timer.setSingleShot(True)
        self.idle_timer.timeout.connect(self.idle_animation)
        self.idle_timer.start(9000)

        # Some Linux window managers drop the always-on-top request after
        # another application receives focus. Re-raise the pet without
        # activating it so it stays visible without stealing keyboard input.
        self.topmost_timer = QTimer(self)
        self.topmost_timer.timeout.connect(self.keep_on_top)
        self.topmost_timer.start(1000)

    def keep_on_top(self):
        self.raise_()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.topmost_timer.stop()
            self.drag_start = event.globalPos()
            self.window_start = self.pos()
            self.dragged = False
            self.system_move_started = False
            window = self.windowHandle()
            if (
                "wayland" in QApplication.platformName().lower()
                and window is not None
                and hasattr(window, "startSystemMove")
            ):
                self.system_move_started = bool(window.startSystemMove())
            event.accept()
        elif event.button() == Qt.RightButton:
            self.show_menu(event.globalPos())
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            delta = event.globalPos() - self.drag_start
            if delta.manhattanLength() > QApplication.startDragDistance():
                self.dragged = True
            if not self.system_move_started:
                self.move(self.window_start + delta)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and not self.dragged:
            self.react()
        self.system_move_started = False
        self.topmost_timer.start(1000)
        event.accept()

    def react(self):
        state, message = random.choice(
            (
                ("happy", "nono 收到！今天也要开心呀～"),
                ("surprised", "哇！你发现嫑嫑啦！"),
                ("zoom", "嫑嫑正在认真看你 👀"),
            )
        )
        self.set_state(state, message)
        QTimer.singleShot(4800, lambda: self.set_state("idle"))

    def set_state(self, state, message=""):
        self.state = state
        self.image_label.setPixmap(self.images[state])
        if message:
            self.tip.setText(message)
            self.tip.adjustSize()
            self.tip.move((self.width() - self.tip.width()) // 2, 2)
            self.tip.show()
            self.tip.raise_()
            QTimer.singleShot(3800, self.tip.hide)

    def idle_animation(self):
        if self.state == "idle":
            state, duration = random.choice(
                (
                    ("idle", 4000),
                    ("zoom", 4800),
                    ("tired", 6800),
                    ("curious", 5200),
                    ("box", 7000),
                    ("nervous", 4500),
                    ("lotus", 5800),
                    ("wave", 4500),
                    ("tilted", 4800),
                    ("measure", 6500),
                    ("pout", 5200),
                )
            )
            self.set_state(state)
            QTimer.singleShot(duration, lambda: self.set_state("idle"))
        self.idle_timer.start(random.randint(6500, 11000))

    def show_menu(self, position):
        menu = QMenu(self)
        menu.addAction("叫我一下", self.react)
        menu.addAction(
            "休息一会儿", lambda: self.set_state("tired", "嫑嫑先躺一小会儿…")
        )
        menu.addSeparator()
        menu.addAction("退出嫑嫑", QApplication.quit)
        menu.exec_(position)


def main():
    app = QApplication(sys.argv)
    pet = NonoPet()
    pet.show()
    pet.raise_()
    raise SystemExit(app.exec_())


if __name__ == "__main__":
    main()
