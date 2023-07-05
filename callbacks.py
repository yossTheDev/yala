import pyalpm

from rich.progress import Progress
from rich.panel import Panel
from rich.spinner import Spinner
from printer import print
from rich.live import Live


def log_cb(level, message):
    if level & pyalpm.LOG_ERROR:
        print(f"[bold red]ERROR:[/bold red] {message}")

    elif level & pyalpm.LOG_WARNING:
        print(f"[bold yellow]WARNING:[/bold yellow] {message}")

    elif level & pyalpm.LOG_DEBUG:
        print(f"[bold bright_black]DEBUG:[/bold bright_black] {message}")

    elif level & pyalpm.LOG_FUNCTION:
        print(f"[bold white]FUNCTION:[/bold white] {message}")


def create_progress_panel():
    prog = Progress()
    progressPanel = Panel(title="Downloading...", renderable=prog)  # type: ignore
    task = prog.add_task(description="Downloading...")  # type: ignore
    return [prog, progressPanel, task]


[_prog, _panel, _task] = create_progress_panel()


_last_target: str = ""
_last_pkg = 0

panel = Panel(title="Downloading", renderable="")


def progress_callback(target, percent, n, i):
    global _last_target, _last_pkg

    if _last_target != target:
        _last_pkg = i
        _last_target = target

        # print(f"{target} {percent} {n} {i}")

        spinner = Spinner(name="bouncingBar", text=f"downloading...{target}")

        panel.title = f"Downloading {i}/{n}"
        panel.renderable = spinner

        # print(panel)

        # _prog.update(
        #    task_id=_task,
        #    description=f"{target}",
        #    completed=0,
        #    total=100,
        # )
        print(_panel)

        # print(f"last:{_last_target} target:{target}")

    # else:
    # print(f"son iguales {percent}")
    # _prog.update(
    #    task_id=_task,
    #    description=f"{target}",
    #    completed=percent,
    #    total=100,
    # )


_last_dl_filename: str = ""
_last_dl_progress = 0
_last_dl_total = 0


def createProgressPanel(filename):
    spinner = Spinner(name="dots", text=f"Downloading...[blue]{filename}[/blue]")
    progressPanel = Panel(
        title="[bold white]Downloading...[/bold white]",
        renderable=spinner,
        title_align="left",
        border_style="green",
    )  # type: ignore
    return progressPanel


live = Live(createProgressPanel(""))
last_dl_filename: str = ""


def dl_cb(filename: str, current, total):
    global last_dl_filename, _last_dl_progress, _last_dl_total

    live.start()

    if filename != last_dl_filename:
        live.update(createProgressPanel(filename=filename))
        last_dl_filename = filename
