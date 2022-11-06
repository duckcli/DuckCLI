from rich.table import Table


def generate_dynamic_table(**kwargs) -> Table:
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
    return table
