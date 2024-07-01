#!/usr/bin/env python3
"""
Mastodon User Search Script
Created by inforensics.ai

This script searches for a Mastodon user across multiple instances.
It uses the instances.social API to fetch a list of instances to search,
or allows the user to specify their own list of instances.
"""

import requests
import concurrent.futures
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

INSTANCES_API_KEY = os.getenv('INSTANCES_API_KEY')

def get_instances_from_api(count=100, min_users=1000, include_down=False, include_closed=False):
    url = "https://instances.social/api/v1/instances/list"
    params = {
        "count": count,
        "min_users": min_users,
        "include_down": str(include_down).lower(),
        "include_closed": str(include_closed).lower(),
        "sort_by": "active_users",
        "sort_order": "desc"
    }
    headers = {"Authorization": f"Bearer {INSTANCES_API_KEY}"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return [instance['name'] for instance in data['instances']]
    except requests.RequestException as e:
        print(f"Error fetching instances: {e}")
        return []

def get_instances_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except IOError as e:
        print(f"Error reading file: {e}")
        return []

def search_user(instance, username, verbose=False):
    if verbose:
        print(f"Searching {instance}...")
    try:
        url = f"https://{instance}/api/v1/accounts/search?q={username}&limit=1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            results = response.json()
            if results and results[0]['username'].lower() == username.lower():
                return {
                    'instance': instance,
                    'account': results[0]
                }
        if verbose:
            print(f"User not found on {instance}")
    except requests.RequestException as e:
        if verbose:
            print(f"Error searching {instance}: {str(e)}")
    return None

def search_mastodon_users(username, instances, verbose=False):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_instance = {executor.submit(search_user, instance, username, verbose): instance for instance in instances}
        for future in concurrent.futures.as_completed(future_to_instance):
            result = future.result()
            if result:
                return result
    return None

def main():
    description = "Search for a Mastodon user across multiple instances."
    epilog = ("Created by inforensics.ai\n"
              "Report bugs to jascha@inforensics.ai")

    parser = argparse.ArgumentParser(description=description, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("username", help="The Mastodon username to search for")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of instances to search (default: 100)")
    parser.add_argument("-m", "--min-users", type=int, default=1000, help="Minimum number of users an instance should have (default: 1000)")
    parser.add_argument("--include-down", action="store_true", help="Include down instances in the search")
    parser.add_argument("--include-closed", action="store_true", help="Include instances with closed registrations")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-i", "--instances", nargs='+', help="List of Mastodon instances to search")
    parser.add_argument("-f", "--file", help="File containing a list of Mastodon instances to search")
    
    args = parser.parse_args()
    
    print("Mastodon User Search Script")
    print("Created by inforensics.ai")
    print()

    if args.verbose:
        print("Verbose mode enabled")
    
    if args.instances:
        instances = args.instances
        print(f"Using {len(instances)} instances provided via command line.")
    elif args.file:
        instances = get_instances_from_file(args.file)
        print(f"Using {len(instances)} instances from file: {args.file}")
    else:
        print("Fetching list of instances from API...")
        instances = get_instances_from_api(count=args.count, min_users=args.min_users, 
                                           include_down=args.include_down, include_closed=args.include_closed)
    
    if not instances:
        print("No instances available to search. Please check your input or API key.")
        return
    
    print(f"Searching for user @{args.username} across {len(instances)} instances...")
    result = search_mastodon_users(args.username, instances, args.verbose)
    
    if result:
        account = result['account']
        print(f"\nUser found on {result['instance']}:")
        print(f"Username: @{account['username']}")
        print(f"Display name: {account['display_name']}")
        print(f"Account URL: {account['url']}")
    else:
        print(f"\nUser @{args.username} not found on any of the searched instances.")

if __name__ == "__main__":
    main()
