import typer
import pyalpm
import pycman
import time
import socket
from typing import List

from rich.console import Console
from rich import print
from rich import prompt
from rich.tree import Tree
from rich.padding import Padding
from rich.text import Text
from rich.panel import Panel

from callbacks import (
    cb_dl,
    cb_progress,
    log_callback,
    new_dl_cb,
)


app = typer.Typer()
console = Console()
pacman = pycman.config.init_with_config("/etc/pacman.conf")  # type: ignore


# App Commands


@app.callback()
def main(verbose: bool = False):
    if verbose == True:
        pacman.logcb = log_callback


@app.command(name="list")
def lis(upgradable: bool = False):
    """
    List all installed or upgradable packages in this machine
    """

    if upgradable == True:
        show_upgradable_packages()
    else:
        show_installed_packages()


@app.command()
def update(verbose: bool = False):
    """
    Update System Databases
    """

    dbs = pacman.get_syncdbs()
    # pacman.dlcb = download_callback

    # Is Verbose Enabled Show Log to the Console
    if verbose == True:
        pacman.logcb = log_callback
    else:
        pacman.logcb = None

    update = ""

    failed = 0

    # Updating Databases
    with console.status("[bold white]Updating Databases...[/bold white]") as status:
        time.sleep(1)
        for db in dbs:
            time.sleep(1)

            try:
                db.update(False)
                status.update(
                    f"[bold white]Updating....[/bold white] [blue]{db.name}[/blue]"
                )
                console.print(
                    f"[bold green]SUCCESS[/bold green] Updating: [blue]{db.name}[blue]"
                )
            except:
                console.print(
                    f"[bold red]ERROR[/bold red] Updating: [blue]{db.name}[/blue]"
                )
                failed = failed + 1

    if failed == len(dbs):
        console.print(
            "[bold yellow] HINT[/bold yellow] Set [white]--verbose[/white] flag to show log about updating process"
        )

    # zh = alpm_handle.init_transaction(booleans)
    # print(zh)


@app.command()
def upgrade(downgrade: bool = False, verbose: bool = False):
    """
    Execute System Upgrade
    """
    if verbose == True:
        pacman.logcb = log_callback
    else:
        pacman.logcb = None

    # Initialize Transaction
    t: pyalpm.Transaction = pacman.init_transaction()
    t.sysupgrade(downgrade)
    t.prepare()

    # Show all upgradable packages
    upgradable = get_upgradable_packages()
    console.print(
        f"There are {str(len(upgradable))} packages with a new version",
        justify="center",
    )

    names = ", ".join([f"{pkg.name}" for pkg in upgradable])

    text = Text(names, style="blue")
    panel = Panel(text, height=10)
    p = Padding(panel, 1)
    console.print(p)

    total_install_size = 0
    total_download_size = 0

    # Show total install and download size
    for pkg in upgradable:
        total_download_size += pkg.download_size
        total_install_size += pkg.isize

    print(
        f"   [bright_black]Total Download Size:[/bright_black] [blue]{relative_bytes_converter(total_download_size)}[blue]"
    )
    print(
        f"   [bright_black]Total Install Size:[/bright_black] [blue]{relative_bytes_converter(total_install_size)}[blue]"
    )

    console.print(
        "[white]Type [green]yala list[/green] [blue]--upgradable[/blue] to se all[/white]",
        justify="center",
    )

    if len(t.to_add) + len(t.to_remove) == 0:
        print("nothing to do")
    else:
        try:
            t.commit()
        except:
            print(f" [bold red]ERROR[/bold red] Upgrading the System [blue]")
            print(
                "[bold yellow] HINT[/bold yellow] Set [white]--verbose[/white] flag to show logs"
            )

    t.release()


@app.command()
def install(pkg: List[str], verbose: bool = False):
    global _last_filename
    """
    Install new packages in the System
    """
    # Initialize Pacman
    # pacman.dlcb = download_callback
    # pacman.progresscb = progress_callback
    # pacman.eventcb = cb_event
    pacman.dlcb = new_dl_cb
    # pacman.progresscb = cb_progress

    # Configure verbosity of this command
    if verbose == True:
        pacman.logcb = log_callback
    else:
        pacman.logcb = None

    # Get Sync DBs
    dbs = pacman.get_syncdbs()

    # Initialize New Transaction
    try:
        t: pyalpm.Transaction = pacman.init_transaction()

        # Search for Packages To Install
        packages_to_install = list(set(pkg))
        pkgs = []

        for package in packages_to_install:
            pk = get_package(package, dbs)

            if pk:
                # Add package to the Transaction
                t.add_pkg(pk)
                pkgs.append(pk)
            else:
                print(f"[bold red]ERROR[/bold red] Package {package} not found")

        # Install valid packages
        if len(pkgs) != 0:
            # Show to the user the packages to be installed
            names = ", ".join([f"[blue]{pkg.name}[/blue]" for pkg in pkgs])
            print(f" Do you want to install ({str(len(pkgs))}) packages: {names}?")

            # Show download and install total size
            total_download_size = 0
            total_install_size = 0

            for pkg in pkgs:
                total_download_size += pkg.download_size  # type: ignore
                total_install_size += pkg.isize  # type: ignore

            print(
                f"   [bright_black]Total Download Size:[/bright_black] [blue]{relative_bytes_converter(total_download_size)}[blue]"
            )
            print(
                f"   [bright_black]Total Install Size:[/bright_black] [blue]{relative_bytes_converter(total_install_size)}[blue]"
            )

            print()

            if prompt.Confirm.ask("  [white bold]Continue?[/white bold]"):
                # Resolve Dependencies
                result = t.prepare()

                # if not result:
                # print("[bold red]ERROR Resolving dependencies [/bold red]")

                # Commit Transaction
                try:
                    t.commit()
                    print(f" Package/s ({names}) are suceffuly installed")
                # print(f" [bold red]ERROR[/bold red] No internet connection")

                except Exception as error:
                    print(f" [bold red]ERROR[/bold red] Resolving Packages")

        # Realease Transaction
        t.release()
    except pyalpm.error as error:
        print(f" [bold red]ERROR[/bold red] {error.args[0]}")


@app.command()
def search(query: str, local: bool = False, exact: bool = False):
    """
    Search for packages in local and sync dbs
    """

    if local == True:
        search_localdb(query, exact)
    else:
        search_syncdbs(query, exact)


# Utils


def show_upgradable_packages():
    upgradable = 0

    for pkg in pacman.get_localdb().pkgcache:
        for sync_db in pacman.get_syncdbs():
            sync_pkg = sync_db.get_pkg(pkg.name)

            if (
                sync_pkg is not None
                and pyalpm.vercmp(sync_pkg.version, pkg.version) > 0
            ):
                tree = Tree(f"[bold green]{pkg.name}[/bold green]")
                tree.add(f"[white]{pkg.desc}[white]")
                tree.add(
                    f"[bright_black]source[/bright_black] : [blue]{pkg.db.name}[/blue]"
                )
                tree.add(
                    f"[bright_black]install size[/bright_black] : [blue]{relative_bytes_converter(pkg.isize)}[/blue]"
                )
                tree.add(
                    f"[bright_black]version[/bright_black] : {pkg.version} ->  [bold blue]{sync_pkg.version}[/bold blue]"
                )

                p = Padding(tree, 1)

                upgradable = upgradable + 1

                print(p)

    if upgradable == 0:
        console.print(
            "[bold white]Congrats your system is [blue]Up To Date[/blue][/bold white]",
            justify="center",
        )
        console.print("[bold white]Nothing to do here[/bold white]", justify="center")
    else:
        console.print(
            f"[bold white]Total Upgradable Packages: [/bold white] [green] {upgradable} [/green]",
            justify="center",
        )


def get_upgradable_packages():
    upgradable = []

    for pkg in pacman.get_localdb().pkgcache:
        for sync_db in pacman.get_syncdbs():
            sync_pkg = sync_db.get_pkg(pkg.name)

            if (
                sync_pkg is not None
                and pyalpm.vercmp(sync_pkg.version, pkg.version) > 0
            ):
                upgradable.append(sync_pkg)

    return upgradable


def show_installed_packages():
    db = pacman.get_localdb()

    for pkg in db.pkgcache:
        tree = Tree(f"[bold green]{pkg.name}[/bold green]")
        tree.add(f"[white]{pkg.desc}[white]")
        tree.add(f"[bright_black]source[/bright_black] : [blue]{pkg.db.name}[/blue]")
        tree.add(
            f"[bright_black]install size[/bright_black] : [blue]{relative_bytes_converter(pkg.isize)}[/blue]"
        )
        tree.add(f"[bright_black]version[/bright_black] : {pkg.version}")

        p = Padding(tree, 1)

        print(p)

    console.print(
        f"[bold white]Total Installed Packages: [/bold white] [green] {len(db.pkgcache)} [/green]",
        justify="center",
    )


def progress(percent, message):
    typer.echo(percent)


def get_package(package: str, dbs):
    for db in dbs:
        pk = db.get_pkg(package)
        if pk:
            return pk
    return None


def search_localdb(query: str, exact: bool):
    """
    Search Packages in Local DB
    """
    db: pyalpm.DB = pacman.get_localdb()

    if exact == True:
        pkg = db.get_pkg(query)

        if pkg:
            tree = Tree(f"[bold green]{pkg.name}[/bold green]")
            tree.add(f"[white]{pkg.desc}[white]")
            tree.add(
                f"[bright_black]source[/bright_black] : [blue]{pkg.db.name}[/blue]"
            )
            tree.add(
                f"[bright_black]install size[/bright_black] : [blue]{relative_bytes_converter(pkg.isize)}[/blue]"
            )
            tree.add(f"[bright_black]version[/bright_black] : {pkg.version}")

            p = Padding(tree, 1)

            print(p)
        else:
            print("Sorry there are not package with this name")
    else:
        pkgs = db.search(query)
        pkgs.reverse()

        for pkg in pkgs:
            tree = Tree(f"[bold green]{pkg.name}[/bold green]")
            tree.add(f"[white]{pkg.desc}[white]")
            tree.add(
                f"[bright_black]source[/bright_black] : [blue]{pkg.db.name}[/blue]"
            )
            tree.add(
                f"[bright_black]install size[/bright_black] : [blue]{relative_bytes_converter(pkg.isize)}[/blue]"
            )
            tree.add(f"[bright_black]version[/bright_black] : {pkg.version}")

            p = Padding(tree, 1)

            print(p)


def search_syncdbs(query: str, exact: bool):
    """
    Search Packages in Sync DBs
    """
    dbs = pacman.get_syncdbs()

    pkgs = []

    if exact == True:
        pkg = get_package(query, dbs)

        if pkg:
            tree = Tree(f"[bold green]{pkg.name}[/bold green]")
            tree.add(f"[white]{pkg.desc}[white]")
            tree.add(
                f"[bright_black]source[/bright_black] : [blue]{pkg.db.name}[/blue]"
            )
            tree.add(
                f"[bright_black]install size[/bright_black] : [blue]{relative_bytes_converter(pkg.isize)}[/blue]"
            )
            tree.add(
                f"[bright_black]download size[/bright_black] : [blue]{relative_bytes_converter(pkg.download_size)}[/blue]"
            )
            tree.add(f"[bright_black]version[/bright_black] : {pkg.version}")

            p = Padding(tree, 1)

            print(p)
        else:
            print("Sorry there are not package with this name")

    else:
        for db in dbs:
            pkg = db.search(query)
            pkgs.extend(pkg)

        pkgs.reverse()

        for pkg in pkgs:
            tree = Tree(f"[bold green]{pkg.name}[/bold green]")
            tree.add(f"[white]{pkg.desc}[white]")
            tree.add(
                f"[bright_black]source[/bright_black] : [blue]{pkg.db.name}[/blue]"
            )
            tree.add(
                f"[bright_black]install size[/bright_black] : [blue]{relative_bytes_converter(pkg.isize)}[/blue]"
            )
            tree.add(
                f"[bright_black]download size[/bright_black] : [blue]{relative_bytes_converter(pkg.download_size)}[/blue]"
            )
            tree.add(f"[bright_black]version[/bright_black] : {pkg.version}")

            p = Padding(tree, 1)

            print(p)


def get_download_size(pkg: pyalpm.Package):
    dbs = pacman.get_syncdbs()

    size = pkg.download_size

    if pkg.depends:
        for dep in pkg.depends:
            pk = get_package(dep, dbs)
            if pk is not None:
                # size += get_dep_size(pk)
                installed_pkg = pacman.get_localdb().get_pkg(pk.name)

                if installed_pkg is None or installed_pkg.version != pk.version:
                    size += pk.download_size

    return size


def get_install_size(pkg: pyalpm.Package):
    dbs = pacman.get_syncdbs()

    size = pkg.isize

    if pkg.depends:
        for dep in pkg.depends:
            pk = get_package(dep, dbs)
            if pk is not None:
                # size += get_dep_size(pk)
                installed_pkg = pacman.get_localdb().get_pkg(pk.name)

                if installed_pkg is None or installed_pkg.version != pk.version:
                    size += pk.isize

    return size


def relative_bytes_converter(num_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f}{unit}"
        num_bytes /= 1024

    return f"{num_bytes:.1f}PB"


def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError as error:
        print(error)
        return False


app()
