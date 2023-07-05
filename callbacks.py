import sys
import pyalpm
import math

from rich.progress import Progress
from rich.panel import Panel
from rich.spinner import Spinner
from rich.console import Console
from printer import print
from rich.live import Live


def log_callback(level, message):
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


def download_callback(filename: str, current, total):
    global _last_dl_filename, _last_dl_progress, _last_dl_total, _prog, _panel, _task, _total_pkgs

    # check if a new file is coming
    if filename != _last_dl_filename or _last_dl_total != total:
        _last_dl_total = total
        _last_dl_progress = 0
        _last_dl_filename = filename

        print(f"filename:{filename} lastfilename{_last_dl_filename}")
        sys.stdout.write("\ndownload %s: %d/%d" % (filename, current, total))

        _panel.title = f"Downloading {current}/{total} packages"

        _prog.update(
            task_id=_task,
            description=f"{filename}",
            completed=current,
            total=total,
        )

        print(_panel)

    else:
        _prog.update(
            task_id=_task,
            description=f"{filename}",
            completed=current,
            total=total,
        )

    # Progress Indicator
    if _last_dl_total > 0:  # type: ignore
        progress = (current * 25) // _last_dl_total
    else:
        # if total is unknown, use log(kBytes)²/2
        progress = int(math.log(1 + current / 1024) ** 2 / 2)
    if progress > _last_dl_progress:  # type: ignore
        _last_dl_progress = progress

        _prog.update(
            task_id=_task,
            description=f"{filename}",
            completed=progress,
            total=100,
        )


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

total_pkgs = None
last_dl_filename: str = ""
console = Console()


def cb_dl(filename, tx, total):
    global _last_dl_filename, _last_dl_progress, _last_dl_total
    # check if a new file is coming
    if filename != _last_dl_filename or _last_dl_total != total:
        _last_dl_filename = filename
        _last_dl_total = total
        _last_dl_progress = 0
        sys.stdout.write("\ndownload %s: %d/%d" % (filename, tx, total))
        sys.stdout.flush()
    # compute a progress indicator

    if _last_dl_total > 0:
        progress = (tx * 25) // _last_dl_total
        print(f"progress: -> {progress}")

    else:
        # if total is unknown, use log(kBytes)²/2
        progress = int(math.log(1 + tx / 1024) ** 2 / 2)
    if progress > _last_dl_progress:
        _last_dl_progress = progress
        sys.stdout.write(
            "\rdownload -> %s: %s %d/%d" % (filename, "." * progress, tx, total)
        )
        sys.stdout.flush()


def new_dl_cb(filename: str, current, total):
    global last_dl_filename, _last_dl_progress, _last_dl_total

    live.start()

    if filename != last_dl_filename:
        live.update(createProgressPanel(filename=filename))
        last_dl_filename = filename


last_target = None
last_percent = 100
last_i = -1


def cb_progress(target, percent, n, i):
    "Display progress percentage for target i/n"
    global last_target, last_percent, last_i
    if len(target) == 0:
        # abstract progress
        if percent < last_percent or i < last_i:
            sys.stdout.write("progress (%d targets)" % n)
            last_i = 0
        sys.stdout.write((i - last_i) * ".")
        sys.stdout.flush()
        last_i = i
    else:
        # progress for some target (write 25 dots for 100%)
        if target != last_target or percent < last_percent:
            last_target = target
            last_percent = 0
            sys.stdout.write("progress for %s (%d/%d)" % (target, i, n))
        old_dots = last_percent // 4
        new_dots = percent // 4
        sys.stdout.write((new_dots - old_dots) * ".")
        sys.stdout.flush()

    # final newline
    if percent == 100 and last_percent < 100:
        sys.stdout.write("\n")
        sys.stdout.flush()
    last_percent = percent
