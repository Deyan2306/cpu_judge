import os
import sys
import tty
import termios
import random
import psutil
import select as std_select
from pipe import select, enumerate

from rich.live import Live
from rich.table import Table
from rich.text import Text

ROASTS = {
    "idle": [
        "U AFK??", "Bozo, PC is bored :p", "Bro opened Vim and called it a day.",
        "Netflix buffering or what?", "This core just took a nap.", "Congrats, you mastered doing nothing!"
    ],
    "working": [
        "Respectable, respectable..", "Something productive maybe?", "Mid-tier effort detected, still a nerd.",
        "Keep grinding, but not too hard.", "Yo, yo, this core got its coffee ready.", "Excel works harder than this."
    ],
    "melting": [
        "Are you fr, bro, this aint a stove ;(", "Bro, let me breathe....", "This PC is fighting for its life, fr",
        "This aint your oven bro, wtf", "Reaching sun-like temperatures", "Im impressed, really"
    ]
}

class KeyListener:
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        try:
            self.old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        except Exception:
            self.old = None
        return self

    def __exit__(self, *args):
        if self.old:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)

    def key_pressed(self):
        # Uses the renamed std_select
        return std_select.select([sys.stdin], [], [], 0)[0]

    def read_key(self):
        return sys.stdin.read(1)

def cpu_core_stream():
    while True:
        yield psutil.cpu_percent(interval=1, percpu=True)

def classify(cpu):
    if cpu < 15: return "idle"
    if cpu < 60: return "working"
    return "melting"

def get_row_data(item):
    """Logic for a single core's data packet."""
    idx, cpu = item
    level = classify(cpu)
    return {
        "core": f"Core {idx}",
        "cpu": cpu,
        "level": level,
        "msg": random.choice(ROASTS[level])
    }

def make_table(rows):
    table = Table(title="[bold cyan]System Roast Monitor[/]")
    table.add_column("Core", justify="right")
    table.add_column("CPU %", justify="right")
    table.add_column("Mood")
    table.add_column("Judgement")

    colors = {"idle": "green", "working": "yellow", "melting": "red"}

    for r in rows:
        color = colors[r["level"]]
        table.add_row(
            r["core"],
            f"{r['cpu']:>5.1f}",
            Text(r["level"].upper(), style=color),
            Text(r["msg"], style=color)
        )
    return table

def run():
    os.system("cls" if os.name == "nt" else "clear")

    with KeyListener() as keys:
        with Live(refresh_per_second=4, screen=True) as live:
            for usages in cpu_core_stream():
                if keys.key_pressed() and keys.read_key() == "q":
                    break

                rows = list(
                    usages
                    | enumerate
                    | select(lambda x: get_row_data(x))
                )

                table = make_table(rows)
                table.caption = Text("\nPress q to exit", style="italic")

                live.update(table)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
