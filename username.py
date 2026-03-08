import requests
sites = {
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}",
    "X": "https://x.com/{}",  # formerly Twitter
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Discord": "https://discord.com/users/{}",
    "Bluesky": "https://bsky.app/profile/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Epic Games": "https://www.epicgames.com/id/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "BeReal": "https://www.bereal.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Pinterest": "https://www.pinterest.com/{}",
}

def search_username(username):
    results = {}

    for site, url in sites.items():
        full_url = url.format(username)
        try:
            r = requests.get(full_url, timeout=5)
            if r.status_code == 200:
                results[site] = full_url  
            else:
                results[site] = None
        except requests.RequestException:
            results[site] = None
    return results