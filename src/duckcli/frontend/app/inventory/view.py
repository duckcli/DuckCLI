from rich.table import Table

MAX_ROW = 250
# f"[red]{status}" if status == "ZTP failed" else f"[green]{status}"


def generate_inventory_table(**kwargs) -> Table:
    row_count = 0
    """Make a new table."""
    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("ID")
    table.add_column("Hostname", style="green", no_wrap=True)
    table.add_column("Vendor")
    table.add_column("Model")
    table.add_column("OS Type", style="magenta")
    table.add_column("Mgmt Ip")
    table.add_column("site Id", style="cyan")
    # input data
    inventory = kwargs.get("inventory")
    for item in inventory:
        table.add_row(
            f"{item.get('id')}",
            f"{item.get('hostname')}",
            f"{item.get('vendor')}",
            f"{item.get('model')}",
            f"{item.get('osType')}",
            f"{item.get('mgmtIp')}",
            f"{item.get('siteId')}",
        )
        row_count += 1
        if row_count == MAX_ROW:
            break
    return table
