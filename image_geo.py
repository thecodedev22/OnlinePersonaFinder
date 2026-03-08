from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

def get_exif_data(image):
    """Extract EXIF data from an image."""
    exif_data = {}
    info = image._getexif()

    if not info:
        return exif_data

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            gps_data = {}
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_data[sub_decoded] = value[t]
            exif_data["GPSInfo"] = gps_data
        else:
            exif_data[decoded] = value

    return exif_data

def convert_to_degrees(value):
    """Convert GPS coordinates to decimal degrees."""
    d = value[0][0] / value[0][1]
    m = value[1][0] / value[1][1]
    s = value[2][0] / value[2][1]
    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Extract latitude and longitude from EXIF GPS data."""
    gps_info = exif_data.get("GPSInfo")
    if not gps_info:
        return None, None

    lat = convert_to_degrees(gps_info["GPSLatitude"])
    if gps_info.get("GPSLatitudeRef") != "N":
        lat = -lat

    lon = convert_to_degrees(gps_info["GPSLongitude"])
    if gps_info.get("GPSLongitudeRef") != "E":
        lon = -lon

    return lat, lon

def extract_image_location(path):
    """Extract GPS coordinates from an image file and return a Google Maps link."""
    if not os.path.exists(path):
        return None

    try:
        image = Image.open(path)
        exif_data = get_exif_data(image)
        lat, lon = get_lat_lon(exif_data)

        if lat is not None and lon is not None:
            return {
                "lat": lat,
                "lon": lon,
                "map": f"https://www.google.com/maps?q={lat},{lon}"
            }

        return None
    except Exception:
        return None