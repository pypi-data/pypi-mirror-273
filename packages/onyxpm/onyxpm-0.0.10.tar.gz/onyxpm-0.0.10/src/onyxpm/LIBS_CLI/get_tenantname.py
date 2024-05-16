from rich.console import Console
import os

def get_tenantname():
    console = Console()
    env_conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../env.conf"))


    # Check if the env.conf file is empty
    if os.path.getsize(env_conf_path) == 0:
        console.print("No tenants are set yet. It seems your env.conf is empty.", style="yellow")
        console.print("Please configure your tenant parameters using the tenant set command.", style="yellow")
        return

    with open(env_conf_path, 'r') as f:
        line_number = 1
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                console.print(f"{line_number}. {line[1:].upper()}", style="yellow")
                line_number += 1