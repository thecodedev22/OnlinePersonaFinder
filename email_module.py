import dns.resolver
import socket
import requests

def check_email(email):
    info = {
        "email": email,
        "valid_format": False,
        "domain": None,
        "mx_records": [],
        "domain_live": False,
        "https": False,
        "catch_all": False,
        "company": None
    }

    # Validate format
    import re
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, email):
        info["valid_format"] = True

    # Extract domain
    try:
        domain = email.split("@")[1]
        info["domain"] = domain
    except IndexError:
        return info

    # MX records
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        info["mx_records"] = [str(rdata.exchange) for rdata in answers]
    except Exception:
        pass

    # Check if domain is live
    try:
        resp = requests.get(f"http://{domain}", timeout=5)
        if resp.status_code < 400:
            info["domain_live"] = True
            if resp.url.startswith("https://"):
                info["https"] = True
    except Exception:
        pass

    # Optional: get company name from IP
    try:
        ip = socket.gethostbyname(domain)
        geo = requests.get(f"http://ip-api.com/json/{ip}?fields=isp").json()
        info["company"] = geo.get("isp")
    except Exception:
        pass

    # Optional: catch-all detection
    # Note: real SMTP check can be tricky; here we just mark false
    info["catch_all"] = False

    return info