from rich import print as rprint
from rich.align import Align
from rich.console import Console
from rich.json import JSON
from rich.padding import Padding
from rich.panel import Panel

console = Console()


def write_results(filename, errors, warnings, use_emoji=True):
    error_total = 0
    warning_total = 0

    if errors:
        for component, errs in errors.items():
            error_total += len(errs)
    if warnings:
        for component, warns in warnings.items():
            warning_total += len(warns)

    all = coalesce_errors_and_warnings(errors, warnings)

    err_plural = "" if error_total == 1 else "s"
    warn_plural = "" if warning_total == 1 else "s"

    header = Align(Panel(f"[bold green]Parser results for '{filename}':"
    f" [bold red]{error_total} error{err_plural}[/bold red],"
    f" [bold yellow]{warning_total} warning{warn_plural}", style="blue"), align="center")
    console.print(header)

    net_errors = errors.pop("network",[]) if errors else []
    net_warnings = warnings.pop("network",[]) if warnings else []
    net_all = all.pop("network",[])

    if net_all:
        console.rule(f"[bold green]Network", style="blue")
        console.print()
    for eow in net_all:
        if isinstance(eow, Warning):
            prefix = ":yellow_circle:" if use_emoji else "[WARNING]"
            row = "warning"
        else:
            row = "rule"
            prefix = ":red_circle:" if use_emoji else "[FAILURE]"

        line = Padding(f"{prefix}  Network {row} -> [white italic]{eow}[/white italic]", (0,2))
        console.print(line)
    console.print()

    for component, eows in all.items():
        console.rule(f"[bold green]{component.capitalize()}", style="blue")
        console.print()

        for eow in eows:
            if isinstance(eow, Warning):
                prefix = ":yellow_circle:" if use_emoji else eow.desc_text
                row = eow.warning
            else:
                row = eow.rule
                prefix = ":red_circle:" if use_emoji else eow.desc_text

            eow_line = Padding(
            f"{prefix}  {eow.component} [bold blue]'{row}'[/bold blue] ->"
            f" [white italic]{eow.exc}[/white italic]",
            (0, 2))
            value_line = Padding(f"{eow.valuetext}", (0, 12))
            console.print(eow_line)
            console.print(value_line)

        console.print()
    console.rule(style="blue")


def coalesce_errors_and_warnings(errors, warnings):
    warnings = warnings if warnings else {}
    all = errors.copy() if errors else {}

    for component, warns in warnings.items():
        comp_errs = all.get(component, [])
        all[component] = comp_errs + warns

    return all
