import random
import sys
import tkinter as tk
from pathlib import Path


ROOT = (
    Path(sys._MEIPASS)
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent
)
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


class NonoPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("嫑嫑 nono")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        if sys.platform == "darwin":
            self.transparent_bg = "systemTransparent"
            self.root.configure(bg=self.transparent_bg)
            self.root.wm_attributes("-transparent", True)
        else:
            self.transparent_bg = "#ff00ff"
            self.root.configure(bg=self.transparent_bg)
            self.root.wm_attributes("-transparentcolor", self.transparent_bg)

        self.images = {
            name: tk.PhotoImage(file=ASSETS / f"{name}.png")
            for name in ASSET_NAMES
        }
        self.state = "idle"
        self.label = tk.Label(
            self.root,
            image=self.images[self.state],
            bg=self.transparent_bg,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
        )
        self.label.pack()

        self.tip = tk.Label(
            self.root,
            text="",
            font=("Microsoft YaHei UI", 10),
            fg="#332f3a",
            bg="#fff7d6",
            padx=10,
            pady=6,
        )

        self.drag_x = 0
        self.drag_y = 0
        self.dragged = False
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<ButtonRelease-1>", self.release)
        self.label.bind("<Button-3>", self.show_menu)
        self.label.bind("<Button-2>", self.show_menu)
        self.label.bind("<Control-Button-1>", self.show_menu)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="叫我一下", command=self.react)
        self.menu.add_command(label="休息一会儿", command=lambda: self.set_state("tired", "嫑嫑先躺一小会儿…"))
        self.menu.add_separator()
        self.menu.add_command(label="退出嫑嫑", command=self.root.destroy)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"280x280+{sw - 330}+{sh - 380}")
        self.root.after(9000, self.idle_animation)

    def start_drag(self, event):
        self.drag_x = event.x_root - self.root.winfo_x()
        self.drag_y = event.y_root - self.root.winfo_y()
        self.dragged = False

    def drag(self, event):
        self.dragged = True
        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y
        self.root.geometry(f"+{x}+{y}")

    def release(self, _event):
        if not self.dragged:
            self.react()

    def react(self):
        reactions = [
            ("happy", "nono 收到！今天也要开心呀～"),
            ("surprised", "哇！你发现嫑嫑啦！"),
            ("zoom", "嫑嫑正在认真看你 👀"),
        ]
        state, text = random.choice(reactions)
        self.set_state(state, text)
        self.root.after(4800, lambda: self.set_state("idle"))

    def set_state(self, state, message=""):
        self.state = state
        self.label.configure(image=self.images[state])
        if message:
            self.tip.configure(text=message)
            self.tip.place(relx=0.5, y=2, anchor="n")
            self.tip.lift()
            self.root.after(3800, self.tip.place_forget)

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
            self.root.after(duration, lambda: self.set_state("idle"))
        self.root.after(random.randint(6500, 11000), self.idle_animation)

    def show_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        missing = [name for name in ASSET_NAMES if not (ASSETS / f"{name}.png").is_file()]
        raise SystemExit(1 if missing else 0)
    NonoPet().run()
