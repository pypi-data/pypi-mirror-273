import dataclasses
import re
import sys

import rich
import rich.theme
import typer

app = typer.Typer(add_completion=False)

CUSTOM_THEME = rich.theme.Theme(
    {
        "time": "bright_black",
        "prefix": "cyan",
        "debug": "blue",
        "trace": "blue",
        "info": "green",
        "warning": "yellow",
        "error": "red",
        "std": "white",
    }
)


@dataclasses.dataclass
class Line:
    time: str
    prefix: str | None
    level: str
    msg: str
    fields: dict[str, str]


def parse_line(line) -> Line:
    # Define the pattern to match key-value pairs
    pattern = re.compile(r'(\w+)="([^"]+)"|(\w+)=([^"\s]+)')

    # Find all matches in the line
    matches = pattern.findall(line)

    # Iterate over each match
    items = {(match[0] or match[2]): match[1] or match[3] for match in matches}

    time = items.pop("time")
    prefix = items.pop("prefix", None)
    level = items.pop("level")
    msg = items.pop("msg")

    return Line(time=time, prefix=prefix, level=level, msg=msg, fields=items)


@app.command()
def main():
    console = rich.console.Console(theme=CUSTOM_THEME)
    for line in sys.stdin:
        try:
            parsed = parse_line(line)

            fields = (
                f"[{parsed.level}]{key}[/{parsed.level}]=[std]{value}[/std]"
                for key, value in parsed.fields.items()
            )

            msg = (
                f"[time][{parsed.time}][/time]  "
                f"[{parsed.level}]{parsed.level.upper()}[/{parsed.level}] "
                f"[prefix]{parsed.prefix}:[/prefix] "
                f"{parsed.msg} "
                f"{' '.join(fields)}"
            )

            console.print(msg)

        except Exception:
            # If exception, just print the line.
            console.log(line)
