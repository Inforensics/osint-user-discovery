# NAME

tweet-cache-search.py - Search for cached tweets across various archiving and caching services

# SYNOPSIS

`tweet-cache-search.py [-h] [-u USERNAME] [-o]`

# DESCRIPTION

`tweet-cache-search.py` is a Python script that searches for cached tweets of a specified Twitter username across multiple archiving and caching services. It provides links to search results or cached pages from these services and optionally opens the results in your default web browser.

The script searches the following services:

- Wayback Machine
- Google Cache
- Ghost Archive
- Bing
- Yandex
- Baidu
- Internet Archive
- WebCite

# OPTIONS

`-h, --help`
    Show the help message and exit.

`-u USERNAME, --username USERNAME`
    Specify the Twitter username to search for. If not provided, the script will prompt for input.

`-o, --open`
    Open the search results in the default web browser.

# USAGE

1. Ensure you have Python 3 installed on your system.
2. Install the required library:
   ```
   pip install requests
   ```
3. Run the script with desired options:
   ```
   ./tweet-cache-search.py [-u USERNAME] [-o]
   ```

# OUTPUT

The script will display results for each service, showing either a link to the search results/cached page or a message indicating that no results were found. If the `-o` option is used, it will also open successful results in your default web browser.

# EXAMPLES

Search for a specific username:
```
$ ./tweet-cache-search.py -u example_user
```

Search for a username and open results in the browser:
```
$ ./tweet-cache-search.py -u example_user -o
```

Run the script interactively:
```
$ ./tweet-cache-search.py
Enter the Twitter username to search for: example_user
```

# NOTES

- This script provides links to search results or cached pages. It does not scrape or display the actual tweets.
- Some services might have restrictions on automated access. Use this script responsibly and in accordance with each service's terms of use.
- The script's effectiveness depends on the availability and indexing of content by the searched services.
- Opening results in the browser (`-o` option) will attempt to open a new tab or window for each successful result.

# SEE ALSO

- Python Requests library documentation: https://docs.python-requests.org/
- Python argparse module: https://docs.python.org/3/library/argparse.html
- Python webbrowser module: https://docs.python.org/3/library/webbrowser.html

# AUTHOR

This script and man page were created with the assistance of an [Inforensics](https://inforensics.ai) AI language model.

# BUGS

Please report any bugs or issues in Github Issues

# COPYRIGHT

This is free software: you are free to change and redistribute it under the terms of MIT [LICENSE](../LICENSE).
