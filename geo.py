# geo.py
import requests

def lookup_ip(ip):
    """
    Look up IP geolocation using ip-api.com (free, city-level accuracy can vary)
    """
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,lat,lon,isp,query")
        data = resp.json()
        if data.get("status") != "success":
            return None

        return {
            "ip": data.get("query"),
            "country": data.get("country"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "isp": data.get("isp"),
            "map": f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}"
        }
    except Exception:
        return 