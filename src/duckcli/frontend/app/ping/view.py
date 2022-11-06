from rich.table import Table
from rich.panel import Panel
from datetime import datetime
from rich.layout import Layout
from duckcli.frontend.settings.settings import get_settings


cli_settings = get_settings()


# import my_data
STATUS_CHECK_URL = cli_settings.backend_status_check_url

# f"[red]{status}" if status == "ZTP failed" else f"[green]{status}"


def make_ping_check_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="PingMain")

    layout.split(
        Layout(name="header", size=4),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="Ping"),
    )

    return layout


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]DuckCLI[/b] Network UI",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )

        return Panel(grid, style="white on black")


class Footer:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_row(
            "[b]DuckCLI[/b] network facts gathering.......plesse wait ......>>>>>>",
        )

        return Panel(grid, style="white on black")


def generate_pingcheck_table(**kwargs) -> Table:
    """Make a new table."""
    table = Table(show_header=True, header_style="yellow")
    table.add_column("Address", style="white", no_wrap=True)
    table.add_column("Hostname", style="blue", no_wrap=True)
    table.add_column("Is alive", style="cyan")
    table.add_column("Packet loss", style="magenta")
    table.add_column("Avg rtt", style="white")
    table.add_column("Min rtt", style="white")
    table.add_column("Max rtt", style="white")
    table.add_column("Packets sent", style="white")
    table.add_column("Packets received", style="yellow")
    table.add_column("Jitter", style="white")
    ping_response = kwargs.get("ping_response")  # my_data.data1
    for item in ping_response:
        # print(item)
        status = item.get("is_alive")
        table.add_row(
            f"{item.get('address')}",
            f"{item.get('hostname')}",
            f"[green]{status}" if status else f"[red]{status}",
            f"{item.get('packet_loss')}",
            f"{round(int(item.get('avg_rtt')))}",
            f"{round(int(item.get('min_rtt')))}",
            f"{round(int(item.get('max_rtt')))}",
            f"{item.get('packets_sent')}",
            f"{item.get('packets_received')}",
            f"{round(int(item.get('jitter')))}",
        )
    return table


# layout = make_ping_check_layout()
# layout["header"].update(Header())
