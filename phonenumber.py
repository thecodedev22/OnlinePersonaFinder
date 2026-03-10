import re
from urllib.parse import quote_plus

import phonenumbers
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from phonenumbers import carrier, geocoder, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

init(autoreset=True)


def _build_session():
	"""Create a requests session with retries for flaky network responses."""
	retry = Retry(
		total=3,
		connect=3,
		read=3,
		backoff_factor=0.4,
		status_forcelist=(429, 500, 502, 503, 504),
		allowed_methods=("GET",),
	)
	adapter = HTTPAdapter(max_retries=retry)
	session = requests.Session()
	session.mount("http://", adapter)
	session.mount("https://", adapter)
	session.headers.update(
		{
			"User-Agent": (
				"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
				"(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
			)
		}
	)
	return session


def _normalize_input(number):
	"""Trim noisy characters while preserving the leading + sign."""
	number = number.strip()
	number = re.sub(r"(?!^)\+", "", number)
	number = re.sub(r"[^0-9+]", "", number)
	return number


def parse_phone_number(number, region=None):
	"""Parse and validate a phone number with optional region fallback."""
	normalized = _normalize_input(number)
	if not normalized:
		return {"ok": False, "error": "No digits found in the provided phone number."}

	parsed = None
	parse_errors = []

	candidate_regions = []
	if region:
		candidate_regions.append(region.upper())
	candidate_regions.append(None)

	for candidate_region in candidate_regions:
		try:
			parsed = phonenumbers.parse(normalized, candidate_region)
			break
		except phonenumbers.NumberParseException as exc:
			parse_errors.append(str(exc))

	if parsed is None:
		return {
			"ok": False,
			"error": "Could not parse phone number.",
			"details": parse_errors[-1] if parse_errors else "Unknown parse error",
		}

	is_possible = phonenumbers.is_possible_number(parsed)
	is_valid = phonenumbers.is_valid_number(parsed)
	number_type = phonenumbers.number_type(parsed)

	result = {
		"ok": True,
		"input": number,
		"normalized": normalized,
		"e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
		"international": phonenumbers.format_number(
			parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
		),
		"national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
		"is_possible": is_possible,
		"is_valid": is_valid,
		"region_code": phonenumbers.region_code_for_number(parsed),
		"number_type": phonenumbers.PhoneNumberType.to_string(number_type),
		"location": geocoder.description_for_number(parsed, "en"),
		"carrier": carrier.name_for_number(parsed, "en"),
		"timezones": list(timezone.time_zones_for_number(parsed)),
	}
	return result


def search_phone_number_web(number, max_results=8):
	"""Search web pages that mention a number using DuckDuckGo HTML results."""
	query = quote_plus(f'"{number}"')
	url = f"https://duckduckgo.com/html/?q={query}"

	try:
		session = _build_session()
		response = session.get(url, timeout=10)
		response.raise_for_status()
	except requests.RequestException as exc:
		return {"ok": False, "error": f"Search request failed: {exc}", "results": []}

	soup = BeautifulSoup(response.text, "html5lib")
	results = []

	for card in soup.select("div.result"):
		title_tag = card.select_one("a.result__a")
		snippet_tag = card.select_one("a.result__snippet") or card.select_one("div.result__snippet")

		if not title_tag:
			continue

		href = title_tag.get("href", "").strip()
		title = title_tag.get_text(" ", strip=True)
		snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""

		if not href:
			continue

		results.append({"title": title, "url": href, "snippet": snippet})
		if len(results) >= max_results:
			break

	return {"ok": True, "results": results}


def search_phone_number(number, region=None, max_results=8):
	"""Combine local number intelligence with lightweight web search."""
	details = parse_phone_number(number, region=region)
	if not details.get("ok"):
		return {"ok": False, "error": details.get("error"), "details": details.get("details")}

	web = search_phone_number_web(details["e164"], max_results=max_results)
	return {"ok": True, "details": details, "web": web}


def format_phone_cli_report(payload):
	"""Build a colorized text report suitable for argparse mode output."""
	if not payload.get("ok"):
		detail = payload.get("details")
		error_line = f"{Fore.RED}Phone lookup failed: {payload.get('error', 'Unknown error')}"
		if detail:
			error_line += f" ({detail})"
		return error_line

	details = payload["details"]
	lines = [
		f"{Fore.CYAN}Phone Intelligence",
		f"{Fore.GREEN}E164:{Style.RESET_ALL} {details['e164']}",
		f"{Fore.GREEN}International:{Style.RESET_ALL} {details['international']}",
		f"{Fore.GREEN}National:{Style.RESET_ALL} {details['national']}",
		f"{Fore.GREEN}Region:{Style.RESET_ALL} {details.get('region_code') or 'Unknown'}",
		f"{Fore.GREEN}Type:{Style.RESET_ALL} {details.get('number_type')}",
		f"{Fore.GREEN}Valid:{Style.RESET_ALL} {details.get('is_valid')}",
		f"{Fore.GREEN}Possible:{Style.RESET_ALL} {details.get('is_possible')}",
		f"{Fore.GREEN}Location:{Style.RESET_ALL} {details.get('location') or 'Unknown'}",
		f"{Fore.GREEN}Carrier:{Style.RESET_ALL} {details.get('carrier') or 'Unknown'}",
		f"{Fore.GREEN}Timezones:{Style.RESET_ALL} {', '.join(details.get('timezones') or ['Unknown'])}",
	]

	web = payload.get("web", {})
	results = web.get("results", [])
	if not web.get("ok"):
		lines.append(f"{Fore.YELLOW}Web search unavailable:{Style.RESET_ALL} {web.get('error')}")
	elif not results:
		lines.append(f"{Fore.YELLOW}Web search returned no results.{Style.RESET_ALL}")
	else:
		lines.append(f"{Fore.CYAN}Top Web Mentions")
		for index, item in enumerate(results, start=1):
			lines.append(f"{Fore.MAGENTA}{index}.{Style.RESET_ALL} {item['title']}")
			lines.append(f"   {item['url']}")
			if item.get("snippet"):
				lines.append(f"   {item['snippet']}")

	return "\n".join(lines)
