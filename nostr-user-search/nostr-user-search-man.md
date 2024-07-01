# NOSTR-USER-SEARCH(1)

## NAME

nostr-user-search - Search for a Nostr user across multiple relays

## SYNOPSIS

`nostr-user-search` [OPTIONS] IDENTIFIER

## DESCRIPTION

The nostr-user-search script searches for a specified Nostr user across multiple Nostr relays. It can use a default list of relays or allow the user to specify their own list of relays to search.

## OPTIONS

`IDENTIFIER`
    The Nostr user identifier to search for (required). This can be either a public key (npub1... or hex) or a NIP-05 identifier (user@example.com).

`-r`, `--relays` RELAY [RELAY ...]
    List of Nostr relays to search. If not provided, a default list of relays will be used.

`-f`, `--file` FILE
    File containing a list of Nostr relays to search. If provided, this overrides the default relays and the `-r` option.

`-v`, `--verbose`
    Enable verbose output.

## EXAMPLES

Search for a user by public key using the default relays:
    
    nostr-user-search npub1s...

Search for a user by NIP-05 identifier using specific relays:
    
    nostr-user-search -r wss://relay1.com wss://relay2.com user@example.com

Search for a user using relays from a file:
    
    nostr-user-search -f relays.txt npub1s...

Search for a user with verbose output:
    
    nostr-user-search -v npub1s...

## FILES

If using the `-f` option, the specified file should contain one Nostr relay URL per line, each starting with `wss://`.

## EXIT STATUS

0
    Success
1
    Failure (e.g., no relays available, connection error)

## BUGS

Report bugs to jascha@inforensics.ai

## AUTHOR

Created by inforensics.ai

## SEE ALSO

Nostr Protocol: https://github.com/nostr-protocol/nostr
NIP-01 (Basic protocol flow description): https://github.com/nostr-protocol/nips/blob/master/01.md
NIP-05 (Mapping Nostr keys to DNS-based internet identifiers): https://github.com/nostr-protocol/nips/blob/master/05.md
