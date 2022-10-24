import socket
import sys

import pyfiglet
from rich.console import Console
from rich.table import Table

from utils import extractJsonData, threadPoolExecuter

console = Console()


class PScan:

    PORTS_DATA_FILE = "ports.json"

    def __init__(self):
        self.ports_info = {}
        self.open_ports = []
        self.remote_host = ""

    def get_ports_info(self):
        data = extractJsonData(PScan.PORTS_DATA_FILE)
        self.ports_info = {int(k): v for (k, v) in data.items()}

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            self.open_ports.append(port)
        sock.close()

    def show_completion_message(self):
        print()
        if self.open_ports:
            console.print("Scan Completed. Open Ports:", style="green")
            table = Table(show_header=True, header_style="bold green")
            table.add_column("PORTS", style="blue")
            table.add_column("STATES", style="blue", justify="center")
            table.add_column("SERVICES", style="blue")
            for port in self.open_ports:
                table.add_row(str(port), "OPEN", self.ports_info[port])
            console.print(table)
        else:
            console.print(f"No Open Ports Found on Target",
                          style="bold magenta")

    @staticmethod
    def show_startup_message():
        ascii_art = pyfiglet.figlet_format("# PORT SCANNER #")
        console.print(f"[red]{ascii_art}[/red]")
        console.print("#" * 55, style="red")
        console.print(
            "#" * 11, "TCP Port Scanner by @fkkarakurt", "#" * 11, style="white"
        )
        console.print("#" * 55, style="red")
        print()

    @staticmethod
    def get_host_ip_addr(target):
        try:
            ip_addr = socket.gethostbyname(target)
        except socket.gaierror as e:
            console.print(f"{e}. Exiting.", style="bold red")
            sys.exit()
        console.print(
            f"\nIP address acquired: [bold blue]{ip_addr}[/bold blue]")
        return ip_addr

    def initialize(self):
        self.show_startup_message()
        self.get_ports_info()
        try:
            target = console.input("[bold blue]Target: ")
        except KeyboardInterrupt:
            console.print(f"\nRoger that! Exiting.", style="bold red")
            sys.exit()
        self.remote_host = self.get_host_ip_addr(target)
        try:
            input("\nScanner is ready. Press ENTER to run the scanner.")
        except KeyboardInterrupt:
            console.print(f"\nRoger that. Exiting.", style="bold red")
            sys.exit()
        else:
            self.run()

    def run(self):
        threadPoolExecuter(
            self.scan_port, self.ports_info.keys(), len(self.ports_info.keys())
        )
        self.show_completion_message()


if __name__ == "__main__":
    pscan = PScan()
    pscan.initialize()
