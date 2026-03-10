import webbrowser
import argparse
from username import search_username
from email_module import check_email
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table
from geo import lookup_ip
from image_geo import extract_image_location
from phonenumber import search_phone_number, format_phone_cli_report
import time
import shutil

try:
    from pyfiglet import figlet_format
    PYFIGLET_AVAILABLE = True
except ImportError:
    PYFIGLET_AVAILABLE = False

console = Console()

# -------------------- Boot ASCII --------------------
def boot_sequence():
    width = shutil.get_terminal_size().columns

    if PYFIGLET_AVAILABLE:
        # Use pyfiglet with a font that fits well
        if width >= 100:
            font = "slant"
            line1 = figlet_format("Online  Persona", font=font)
            line2 = figlet_format("Finder  v1", font=font)
        else:
            font = "small"
            line1 = figlet_format("Online Persona", font=font)
            line2 = figlet_format("Finder v1", font=font)

        console.print(line1, style="bold cyan", end="")
        console.print(line2, style="bold magenta", end="")
    else:
        # Fallback: simple banner that fits in 60 chars
        banner = [
            "╔══════════════════════════════════════════╗",
            "║      ONLINE  PERSONA  FINDER  v1         ║",
            "║         OSINT Dashboard                  ║",
            "╚══════════════════════════════════════════╝",
        ]
        for line in banner:
            console.print(line, style="bold cyan")

    console.print("\n[bold yellow]Initializing OSINT Dashboard...[/bold yellow]\n")
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


# -------------------- Phone Number Search --------------------
def phone_scan(number=None, region=None, max_results=8, interactive=True):
    if interactive and not number:
        number = inquirer.text(message="Enter the phone number to search:").execute()

    if not number:
        console.print("[red]Phone number is required.[/red]")
        return

    console.print(f"\n[bold cyan]Searching phone number:[/bold cyan] [yellow]{number}[/yellow]\n")

    payload = search_phone_number(number, region=region, max_results=max_results)
    if not payload.get("ok"):
        details = payload.get("details")
        if details:
            console.print(f"[red]Phone lookup failed:[/red] {payload.get('error')} ({details})")
        else:
            console.print(f"[red]Phone lookup failed:[/red] {payload.get('error')}")
        return

    details = payload["details"]

    detail_table = Table(show_header=True, header_style="bold magenta")
    detail_table.add_column("Property")
    detail_table.add_column("Value")
    detail_table.add_row("E164", details.get("e164", "Unknown"))
    detail_table.add_row("International", details.get("international", "Unknown"))
    detail_table.add_row("National", details.get("national", "Unknown"))
    detail_table.add_row("Region", details.get("region_code", "Unknown") or "Unknown")
    detail_table.add_row("Type", details.get("number_type", "Unknown"))
    detail_table.add_row("Valid", str(details.get("is_valid")))
    detail_table.add_row("Possible", str(details.get("is_possible")))
    detail_table.add_row("Location", details.get("location", "Unknown") or "Unknown")
    detail_table.add_row("Carrier", details.get("carrier", "Unknown") or "Unknown")
    detail_table.add_row("Timezones", ", ".join(details.get("timezones") or ["Unknown"]))
    console.print(detail_table)

    web = payload.get("web", {})
    if not web.get("ok"):
        console.print(f"[yellow]Web search unavailable:[/yellow] {web.get('error')}")
        return

    web_results = web.get("results", [])
    if not web_results:
        console.print("[yellow]No web mentions were found for this number.[/yellow]")
        return

    web_table = Table(show_header=True, header_style="bold magenta")
    web_table.add_column("#", style="cyan", width=4)
    web_table.add_column("Title")
    web_table.add_column("URL", style="green")

    choices = []
    for index, item in enumerate(web_results, start=1):
        web_table.add_row(str(index), item.get("title", "Untitled"), item.get("url", ""))
        choices.append({"name": f"{index}. {item.get('title', 'Untitled')}", "value": item.get("url", "")})

    console.print(web_table)

    if interactive:
        selected_links = inquirer.checkbox(
            message="Select mentions to open:",
            choices=choices,
        ).execute()

        for url in selected_links:
            console.print(f"Opening [blue]{url}[/blue] in browser...")
            webbrowser.open(url)

# -------------------- Main Menu --------------------
def main_menu():
    boot_sequence()
    while True:
        choice = inquirer.select(
            message="Select a scan type:",
            choices=[
                "Username Scan",
                "Email Scan",
                "Phone Number Search",
                "IP Geolocation",
                "Image Location Extraction",
                "Exit"
            ]
        ).execute()

        if choice == "Username Scan":
            username_scan()
        elif choice == "Email Scan":
            email_scan()
        elif choice == "Phone Number Search":
            phone_scan()
        elif choice == "IP Geolocation":
            ip_scan()
        elif choice == "Image Location Extraction":
            image_geo_scan()
        else:
            console.print("[bold red]Exiting...[/bold red]")
            break


def parse_args():
    parser = argparse.ArgumentParser(description="OnlinePersonaFinder")
    subparsers = parser.add_subparsers(dest="command")

    phone_parser = subparsers.add_parser("phone", help="Search intelligence for a phone number")
    phone_parser.add_argument("number", help="Phone number to search")
    phone_parser.add_argument(
        "--region",
        help="Default ISO 3166-1 region code when the number has no country code (example: US)",
    )
    phone_parser.add_argument(
        "--max-results",
        type=int,
        default=8,
        help="Maximum number of web mention results to display",
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.command == "phone":
        payload = search_phone_number(args.number, region=args.region, max_results=args.max_results)
        print(format_phone_cli_report(payload))
    else:
        main_menu()
