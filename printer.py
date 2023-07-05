from rich.console import Console

console = Console()


def print(any):
    try:
        console.print(any)
    except:
        pass
