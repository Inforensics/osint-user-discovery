#!/usr/bin/env python3
"""
Nostr User Search Script
Created by inforensics.ai

This script searches for a Nostr user across multiple relays.
It allows users to specify their own list of relays to search.
"""

import asyncio
import argparse
import json
from urllib.parse import urlparse
import ssl
import certifi
import websockets

DEFAULT_RELAYS = [
    "wss://relay.damus.io",
    "wss://relay.nostr.bg",
    "wss://nostr.zebedee.cloud",
    "wss://relay.nostr.band",
    "wss://nos.lol",
]

async def search_user(relay_url, identifier, verbose=False):
    if verbose:
        print(f"Searching {relay_url}...")
    
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    try:
        async with websockets.connect(relay_url, ssl=ssl_context) as websocket:
            # Check if the identifier is a public key (hex string) or a NIP-05 identifier
            if len(identifier) == 64 and all(c in '0123456789abcdef' for c in identifier.lower()):
                # It's likely a public key
                query = {
                    "kinds": [0],  # Metadata event
                    "authors": [identifier],
                }
            else:
                # Treat it as a NIP-05 identifier
                query = {
                    "kinds": [0],  # Metadata event
                    "search": identifier,
                }

            request = json.dumps(["REQ", "search", query])
            await websocket.send(request)

            while True:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                if data[0] == "EVENT" and data[2]["kind"] == 0:
                    content = json.loads(data[2]["content"])
                    return {
                        "relay": relay_url,
                        "pubkey": data[2]["pubkey"],
                        "name": content.get("name", "Unknown"),
                        "display_name": content.get("display_name", "Unknown"),
                        "nip05": content.get("nip05", "Unknown"),
                    }
                elif data[0] == "EOSE":
                    break

    except (websockets.exceptions.WebSocketException, asyncio.TimeoutError) as e:
        if verbose:
            print(f"Error searching {relay_url}: {str(e)}")
    return None

async def search_nostr_users(identifier, relays, verbose=False):
    tasks = [search_user(relay, identifier, verbose) for relay in relays]
    results = await asyncio.gather(*tasks)
    return next((result for result in results if result), None)

def main():
    description = "Search for a Nostr user across multiple relays."
    epilog = ("Created by inforensics.ai\n"
              "Report bugs to jascha@inforensics.ai")

    parser = argparse.ArgumentParser(description=description, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("identifier", help="The Nostr user identifier (public key or NIP-05) to search for")
    parser.add_argument("-r", "--relays", nargs='+', default=DEFAULT_RELAYS,
                        help="List of Nostr relays to search (default: use a predefined list)")
    parser.add_argument("-f", "--file", help="File containing a list of Nostr relays to search")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    print("Nostr User Search Script")
    print("Created by inforensics.ai")
    print()

    if args.verbose:
        print("Verbose mode enabled")
    
    if args.file:
        with open(args.file, 'r') as f:
            relays = [line.strip() for line in f if line.strip()]
        print(f"Using {len(relays)} relays from file: {args.file}")
    else:
        relays = args.relays
        print(f"Using {len(relays)} provided relays.")
    
    if not relays:
        print("No relays available to search. Please check your input.")
        return

    print(f"Searching for user {args.identifier} across {len(relays)} relays...")
    result = asyncio.run(search_nostr_users(args.identifier, relays, args.verbose))
    
    if result:
        print(f"\nUser found on {result['relay']}:")
        print(f"Public Key: {result['pubkey']}")
        print(f"Name: {result['name']}")
        print(f"Display Name: {result['display_name']}")
        print(f"NIP-05: {result['nip05']}")
    else:
        print(f"\nUser {args.identifier} not found on any of the searched relays.")

if __name__ == "__main__":
    main()
