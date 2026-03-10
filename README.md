# Online Persona Finder

An OSINT (Open Source Intelligence) CLI dashboard for investigating online personas. Search usernames across social platforms, analyze email addresses, geolocate IP addresses, and extract GPS data from images — all from an interactive terminal menu.

## Features

- **Username Scan** — Checks 14 platforms (GitHub, Reddit, Instagram, X, LinkedIn, Facebook, Discord, Bluesky, TikTok, Epic Games, Steam, BeReal, Snapchat, Pinterest) for a given username and lets you open matching profiles directly in your browser.
- **Email Scan** — Validates email format, checks MX records, probes domain availability, detects HTTPS, and looks up the hosting ISP.
- **IP Geolocation** — Resolves an IP address to country, region, city, ISP, and generates a Google Maps link.
- **Image Location Extraction** — Reads EXIF GPS metadata from JPEG/PNG images and generates a Google Maps link from the embedded coordinates.

## Requirements

- Python 3.8+

Install dependencies:

```bash
pip install requests dnspython Pillow InquirerPy rich pyfiglet
```

## Installation

```bash
git clone https://github.com/thecodedev22/OnlinePersonaFinder.git
cd OnlinePersonaFinder
pip install requests dnspython Pillow InquirerPy rich pyfiglet
```

## Usage

```bash
python main.py
```

An interactive menu will appear after a short boot sequence:

```
Select a scan type:
  Username Scan
  Email Scan
  IP Geolocation
  Image Location Extraction
  Exit
```

### Username Scan

Enter a username and the tool checks each supported platform. Found profiles are shown in a table with green links. You can then select which profiles to open in your default browser.

### Email Scan

Enter an email address to see:
- Format validity
- Domain and MX records
- Whether the domain is live and uses HTTPS
- The hosting ISP / company

### IP Geolocation

Enter an IPv4 address to retrieve its approximate geographic location (country, region, city, latitude/longitude, ISP) and a Google Maps link.

> **Note:** IP geolocation is approximate and typically resolves to the ISP's location rather than the exact device location.

### Image Location Extraction

Provide the path to a JPEG or PNG image. If the image contains GPS EXIF data, the tool will display the latitude and longitude and generate a Google Maps link.

## Project Structure

```
OnlinePersonaFinder/
├── main.py            # Interactive CLI menu and application entry point
├── username.py        # Username search across social platforms
├── email_module.py    # Email format validation, DNS and domain checks
├── geo.py             # IP address geolocation via ip-api.com
├── image_geo.py       # EXIF GPS extraction from image files
└── requirements.txt   # Python dependencies
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP requests for platform checks and API calls |
| `dnspython` | MX record lookups for email analysis |
| `Pillow` | EXIF data extraction from images |
| `InquirerPy` | Interactive terminal prompts and menus |
| `rich` | Formatted tables and colored console output |
| `pyfiglet` | ASCII art banner on startup (optional) |

## Disclaimer

This tool is intended for educational and ethical OSINT research only. Always ensure you have proper authorization before investigating any individual's online presence. The author is not responsible for misuse of this tool.
