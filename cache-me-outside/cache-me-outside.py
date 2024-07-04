#!/usr/bin/env python3

"""
cache-me-outside.py - Search for cached versions of any URL across various services.
Made by inforensics.ai
"""

import sys
import subprocess

def install_requirements():
    required = {'requests': '2.31.0'}
    for package, version in required.items():
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Attempting to install...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])
            print(f"{package} has been installed.")

install_requirements()

import requests
from urllib.parse import quote_plus, urlparse
import argparse
import webbrowser
import json
import re
import time

def safe_request(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        return f"Error accessing {url}: {str(e)}"

def search_wayback_machine(url):
    wb_url = f"https://web.archive.org/web/*/{url}"
    result = safe_request(wb_url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return {"service": "Wayback Machine", "status": "success", "url": wb_url}
    return {"service": "Wayback Machine", "status": "error", "message": str(result)}

def search_google_cache(url):
    cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
    result = safe_request(cache_url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return {"service": "Google Cache", "status": "success", "url": cache_url}
    return {"service": "Google Cache", "status": "error", "message": str(result)}

def search_bing(url):
    bing_url = f"https://www.bing.com/search?q=url:{quote_plus(url)}"
    result = safe_request(bing_url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        cache_pattern = r'<a href="(https://cc\.bingj\.com/cache\.aspx[^"]+)"[^>]*>Cached<'
        match = re.search(cache_pattern, result.text)
        if match:
            cache_url = match.group(1)
            return {"service": "Bing", "status": "success", "url": cache_url, "search_url": bing_url}
        else:
            return {"service": "Bing", "status": "success", "url": bing_url, "note": "No cached version link found"}
    return {"service": "Bing", "status": "error", "message": str(result)}

def search_yandex(url):
    yandex_url = f"https://yandex.com/search/?text=url:{quote_plus(url)}"
    result = safe_request(yandex_url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        cache_pattern = r'<a href="(https://yandexwebcache\.net[^"]+)"[^>]*>Cached<'
        match = re.search(cache_pattern, result.text)
        if match:
            cache_url = match.group(1)
            return {"service": "Yandex", "status": "success", "url": cache_url, "search_url": yandex_url}
        else:
            return {"service": "Yandex", "status": "success", "url": yandex_url, "note": "No cached version link found"}
    return {"service": "Yandex", "status": "error", "message": str(result)}

def search_baidu(url):
    baidu_url = f"https://www.baidu.com/s?wd=url:{quote_plus(url)}"
    result = safe_request(baidu_url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return {"service": "Baidu", "status": "success", "url": baidu_url}
    return {"service": "Baidu", "status": "error", "message": str(result)}

def search_internet_archive(url):
    ia_url = f"https://archive.org/search.php?query={quote_plus(url)}"
    result = safe_request(ia_url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return {"service": "Internet Archive", "status": "success", "url": ia_url}
    return {"service": "Internet Archive", "status": "error", "message": str(result)}

def search_archive_today(url):
    at_url = f"https://archive.today/{url}"
    result = safe_request(at_url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return {"service": "Archive.today", "status": "success", "url": at_url}
    return {"service": "Archive.today", "status": "error", "message": str(result)}

def main():
    parser = argparse.ArgumentParser(description="Search for cached versions of any URL across various services.")
    parser.add_argument("-u", "--url", help="URL to search for")
    parser.add_argument("-o", "--open", action="store_true", help="Open successful results in default web browser")
    parser.add_argument("-j", "--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        url = input("Enter the URL to search for: ")

    # Ensure the URL has a scheme
    if not urlparse(url).scheme:
        url = "http://" + url

    services = [
        search_wayback_machine,
        search_google_cache,
        search_bing,
        search_yandex,
        search_baidu,
        search_internet_archive,
        search_archive_today
    ]

    results = []
    for service in services:
        result = service(url)
        results.append(result)
        if not args.json:
            if result["status"] == "success":
                print(f"{result['service']} results:")
                print(f"  URL: {result['url']}")
                if "search_url" in result:
                    print(f"  Search URL: {result['search_url']}")
                if "note" in result:
                    print(f"  Note: {result['note']}")
                
                if args.open:
                    webbrowser.open(result["url"])
            else:
                print(f"No results found on {result['service']}: {result['message']}")
            print("-" * 50)
        
        # Add a small delay between requests to be respectful to the services
        time.sleep(1)

    if args.json:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
