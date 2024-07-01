# MASTODON-USER-SEARCH(1)

## NAME

mastodon-user-search - Search for a Mastodon user across multiple instances

## SYNOPSIS

`mastodon-user-search` [OPTIONS] USERNAME

## DESCRIPTION

The mastodon-user-search script searches for a specified Mastodon user across multiple Mastodon instances. It can use the instances.social API to fetch a list of instances to search, or allow the user to specify their own list of instances.

## OPTIONS

`USERNAME`
    The Mastodon username to search for (required).

`-c`, `--count` COUNT
    Number of instances to search when using the API (default: 100).

`-m`, `--min-users` MIN_USERS
    Minimum number of users an instance should have when using the API (default: 1000).

`--include-down`
    Include down instances in the search when using the API.

`--include-closed`
    Include instances with closed registrations when using the API.

`-v`, `--verbose`
    Enable verbose output.

`-i`, `--instances` INSTANCE [INSTANCE ...]
    List of Mastodon instances to search. If provided, the API will not be used.

`-f`, `--file` FILE
    File containing a list of Mastodon instances to search. If provided, the API will not be used.

## EXAMPLES

Search for user 'johndoe' using the default API settings:
    
    mastodon-user-search johndoe

Search for user 'janedoe' on specific instances:
    
    mastodon-user-search -i mastodon.social mstdn.social janedoe

Search for user 'alexsmith' using instances from a file:
    
    mastodon-user-search -f instances.txt alexsmith

Search for user 'sarahbrown' with verbose output:
    
    mastodon-user-search -v sarahbrown

## ENVIRONMENT

`INSTANCES_API_KEY`
    API key for instances.social. Required if using the API to fetch instances.

## FILES

If using the `-f` option, the specified file should contain one Mastodon instance domain per line.

## EXIT STATUS

0
    Success
1
    Failure (e.g., no instances available, API error)

## BUGS

Report bugs to jascha@inforensics.ai

## AUTHOR

Created by inforensics.ai

## SEE ALSO

Mastodon API documentation: https://docs.joinmastodon.org/api/
instances.social API: https://instances.social/api/doc/
