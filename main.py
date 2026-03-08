import webbrowser
from username import search_username
from email_module import check_email
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table
from geo import lookup_ip
from image_geo import extract_image_location
import time

console = Console()

# -------------------- Boot ASCII --------------------
def boot_sequence():
    ascii_art = r"""
________         .__  .__             __________                                        ___________.__            .___          ____   ________ 
\_____  \   ____ |  | |__| ____   ____\______   \ ___________  __________   ____ _____  \_   _____/|__| ____    __| _/__________\   \ /   /_   |
 /   |   \ /    \|  | |  |/    \_/ __ \|     ___// __ \_  __ \/  ___/  _ \ /    \\__  \  |    __)  |  |/    \  / __ |/ __ \_  __ \   Y   / |   |
/    |    \   |  \  |_|  |   |  \  ___/|    |   \  ___/|  | \/\___ (  <_> )   |  \/ __ \_|     \   |  |   |  \/ /_/ \  ___/|  | \/\     /  |   |
\_______  /___|  /____/__|___|  /\___  >____|    \___  >__|  /____  >____/|___|  (____  /\___  /   |__|___|  /\____ |\___  >__|    \___/   |___|
        \/     \/             \/     \/              \/           \/           \/     \/     \/            \/      \/    \/ 
    """
    console.print(ascii_art, style="bold cyan")
    console.print("[bold yellow]Initializing OSINT Dashboard...[/bold yellow]\n")
    for i in range(3):
        console.print(f"[green]Loading{'.' * (i+1)}[/green]")
        time.sleep(0.5)
    console.print("[bold green]Ready![/bold green]\n")

# -------------------- Username Scan --------------------
def username_scan():
    username = inquirer.text(message="Enter the username to search:").execute()
    console.print(f"\n[bold cyan]Searching for username:[/bold cyan] [yellow]{username}[/yellow]\n")

    results = search_username(username)

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Platform")
    table.add_column("Result")

    found_sites = []

    for site, link in results.items():
        if link:
            table.add_row(site, f"[green]{link}[/green]")
            found_sites.append({"name": f"{site} ({link})", "value": link})
        else:
            table.add_row(site, "[red]NOT FOUND[/red]")

    console.print(table)

    if found_sites:
        selected_links = inquirer.checkbox(
            message="Select platforms to open:",
            choices=found_sites,
        ).execute()

        for url in selected_links:
            console.print(f"Opening [blue]{url}[/blue] in browser...")
            webbrowser.open(url)
    else:
        console.print("[red]No platforms found to open.[/red]")

# -------------------- Email Scan --------------------
def email_scan():
    email = inquirer.text(message="Enter the email to check:").execute()
    console.print(f"\n[bold cyan]Checking email:[/bold cyan] [yellow]{email}[/yellow]\n")

    info = check_email(email)

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property")
    table.add_column("Value")

    table.add_row("Email", email)
    table.add_row("Valid Format", str(info["valid_format"]))
    table.add_row("Domain", str(info["domain"]))
    table.add_row("MX Records", ", ".join(info["mx_records"]) if info["mx_records"] else "None")
    table.add_row("Domain Live?", str(info.get("domain_live", "Unknown")))
    table.add_row("HTTPS?", str(info.get("https", "Unknown")))
    table.add_row("Hosting / Company", str(info.get("company", "Unknown")))
    table.add_row("Catch-All", str(info.get("catch_all", "Unknown")))
    table.add_row("Breached?", str(info.get("breached", False)))
    if info.get("breach_data"):
        table.add_row("Breaches", ", ".join(info["breach_data"]))

    console.print(table)

# -------------------- IP Geolocation --------------------
def ip_scan():
    ip = inquirer.text(message="Enter the IP to geolocate:").execute()
    console.print(f"\n[bold cyan]Geolocating IP:[/bold cyan] [yellow]{ip}[/yellow]\n")
    console.print("[yellow]Note: IP geolocation is approximate and may show ISP location, not exact device location.[/yellow]\n")

    info = lookup_ip(ip)

    if info:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Property")
        table.add_column("Value")

        table.add_row("IP", info["ip"])
        table.add_row("Country", info["country"])
        table.add_row("Region", info["region"])
        table.add_row("City", info["city"])
        table.add_row("ISP", info["isp"])
        table.add_row("Latitude", str(info["lat"]))
        table.add_row("Longitude", str(info["lon"]))
        table.add_row("Map", info["map"])

        console.print(table)
    else:
        console.print("[red]Could not retrieve IP information[/red]")

# -------------------- Image Geolocation --------------------
def image_geo_scan():
    path = inquirer.filepath(
        message="Enter the path to the image:",
        validate=lambda x: x.endswith((".jpg", ".jpeg", ".png")),
        only_files=True
    ).execute()

    console.print(f"\n[bold cyan]Extracting geotag from image:[/bold cyan] [yellow]{path}[/yellow]\n")

    info = extract_image_location(path)

    if info:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Property")
        table.add_column("Value")

        table.add_row("Latitude", str(info["lat"]))
        table.add_row("Longitude", str(info["lon"]))
        table.add_row("Map", info["map"])

        console.print(table)
    else:
        console.print("[red]No GPS data found in image.[/red]")

# -------------------- Main Menu --------------------
def main_menu():
    boot_sequence()  # Show ASCII at startup
    while True:
        choice = inquirer.select(
            message="Select a scan type:",
            choices=[
                "Username Scan",
                "Email Scan",
                "IP Geolocation",
                "Image Location Extraction",
                "Exit"
            ]
        ).execute()

        if choice == "Username Scan":
            username_scan()
        elif choice == "Email Scan":
            email_scan()
        elif choice == "IP Geolocation":
            ip_scan()
        elif choice == "Image Location Extraction":
            image_geo_scan()
        else:
            console.print("[bold red]Exiting...[/bold red]")
            break

if __name__ == "__main__":
    main_menu()