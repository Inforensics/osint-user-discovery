#!/usr/bin/env python3

import requests
from urllib.parse import quote_plus
import argparse
import webbrowser

def safe_request(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        return f"Error accessing {url}: {str(e)}"

def search_wayback_machine(username):
    url = f"https://web.archive.org/web/*/https://twitter.com/{username}"
    result = safe_request(url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return f"Wayback Machine results: {url}"
    return f"No results found on Wayback Machine: {result}"

def search_google_cache(username):
    url = f"https://webcache.googleusercontent.com/search?q=cache:https://twitter.com/{username}"
    result = safe_request(url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return f"Google Cache results: {url}"
    return f"No results found on Google Cache: {result}"

def search_ghost_archive(username):
    url = f"https://ghostarchive.org/search?term={username}"
    result = safe_request(url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return f"Ghost Archive results: {url}"
    return f"No results found on Ghost Archive: {result}"

def search_bing(username):
    url = f"https://www.bing.com/search?q=site:twitter.com+{quote_plus(username)}"
    result = safe_request(url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return f"Bing search results: {url}"
    return f"No results found on Bing: {result}"

def search_yandex(username):
    url = f"https://yandex.com/search/?text=site:twitter.com+{quote_plus(username)}"
    result = safe_request(url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return f"Yandex search results: {url}"
    return f"No results found on Yandex: {result}"

def search_baidu(username):
    url = f"https://www.baidu.com/s?wd=site:twitter.com+{quote_plus(username)}"
    result = safe_request(url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return f"Baidu search results: {url}"
    return f"No results found on Baidu: {result}"

def search_internet_archive(username):
    url = f"https://archive.org/search.php?query=twitter.com%2F{username}"
    result = safe_request(url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return f"Internet Archive search results: {url}"
    return f"No results found on Internet Archive: {result}"

def search_webcite(username):
    url = f"http://webcitation.org/query?url=https://twitter.com/{username}"
    result = safe_request(url)
    if isinstance(result, requests.Response) and result.status_code == 200:
        return f"WebCite results: {url}"
    return f"No results found on WebCite: {result}"

def main():
    parser = argparse.ArgumentParser(description="Search for cached tweets across various services.")
    parser.add_argument("-u", "--username", help="Twitter username to search for")
    parser.add_argument("-o", "--open", action="store_true", help="Open results in default web browser")
    args = parser.parse_args()

    if args.username:
        username = args.username
    else:
        username = input("Enter the Twitter username to search for: ")

    services = [
        search_wayback_machine,
        search_google_cache,
        search_ghost_archive,
        search_bing,
        search_yandex,
        search_baidu,
        search_internet_archive,
        search_webcite
    ]

    for service in services:
        result = service(username)
        print(result)
        if args.open and "results:" in result:
            url = result.split(": ")[1]
            webbrowser.open(url)
        print("-" * 50)

if __name__ == "__main__":
    main()
