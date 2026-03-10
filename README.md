# Online Persona Finder 🔍

An interactive OSINT (Open Source Intelligence) dashboard tool for searching and gathering information about online personas across multiple platforms and data sources.

## Features

- **Username Search**: Search for a username across 20+ social media and gaming platforms
  - GitHub, Reddit, Instagram, X (Twitter), LinkedIn, Facebook, Discord, Bluesky, TikTok, Epic Games, Steam, BeReal, Snapchat, Pinterest, Twitch, Spotify, YouTube, Medium, Dev.to, and HackerNews

- **Email Verification**: Check email validity and gather information
  - Email format validation
  - Domain existence verification
  - MX records lookup
  - Domain live status check
  - SSL/HTTPS support detection

- **Phone Number Lookup**: Search and analyze phone numbers
  - Carrier information
  - Geographic location
  - Timezone information
  - Reverse phone lookup

- **IP Geolocation**: Lookup geographic information from IP addresses
  - Country, city, region details
  - ISP information
  - GPS coordinates

- **Image Geolocation**: Extract location data from images
  - EXIF data extraction
  - Geographic coordinates from images

- **Interactive CLI**: User-friendly terminal interface with rich formatting
  - Color-coded output
  - Interactive menus and checkboxes
  - Tabular result display
  - Direct browser integration

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/thecodedev22/OnlinePersonaFinder.git
cd OnlinePersonaFinder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python main.py
```

The interactive dashboard will present you with options to:
1. **Search Username** - Look up a username across multiple platforms
2. **Check Email** - Verify and analyze an email address
3. **Search Phone Number** - Look up information about a phone number
4. **IP Geolocation** - Check location information for an IP address
5. **Image Geolocation** - Extract location data from images

### Example Workflow

```
$ python main.py

╔══════════════════════════════════════════╗
║      ONLINE  PERSONA  FINDER  v1         ║
║         OSINT Dashboard                  ║
╚══════════════════════════════════════════╝

Select an option:
> Search Username
  Check Email
  Search Phone Number
  IP Geolocation
  Image Geolocation
```

## Dependencies

The project requires the following Python packages:

- `requests` - HTTP library for making web requests
- `InquirerPy` - Interactive CLI for user input
- `rich` - Rich terminal formatting
- `dnspython` - DNS lookup capabilities
- `Pillow` - Image processing
- `pyfiglet` - ASCII art text rendering
- `BeautifulSoup4` - HTML parsing
- `phonenumbers` - Phone number processing
- `colorama` - Cross-platform colored terminal text

All dependencies are listed in `requirements.txt`.

## Project Structure

```
OnlinePersonaFinder/
├── main.py              # Main entry point
├── username.py          # Username search functionality
├── email_module.py      # Email verification
├── phonenumber.py       # Phone number lookup
├── geo.py               # IP geolocation
├── image_geo.py         # Image geolocation
├── requirements.txt     # Project dependencies
├── scan_history.json    # Scan history tracking
└── README.md            # This file
```

## Legal Notice

This tool is designed for **educational and authorized security research purposes only**. Users are responsible for ensuring they comply with all applicable laws and regulations in their jurisdiction when using this tool. Unauthorized access to computer systems or data is illegal.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Disclaimer**: This tool is for educational purposes. Use responsibly and ethically.
