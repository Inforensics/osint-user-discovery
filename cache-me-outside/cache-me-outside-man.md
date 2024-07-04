# NAME

cache-me-outside.py - Search for cached versions of any URL across various caching and archiving services

# SYNOPSIS

`cache-me-outside.py [-h] [-u URL] [-o] [-j]`

# DESCRIPTION

`cache-me-outside.py` is a Python script that searches for cached versions of a specified URL across multiple caching and archiving services. It provides links to search results or cached pages from these services and optionally opens the results in your default web browser.

Created by inforensics.ai

The script searches the following services:

- Wayback Machine
- Google Cache
- Bing
- Yandex
- Baidu
- Internet Archive
- Archive.today

# OPTIONS

`-h, --help`
    Show the help message and exit.

`-u URL, --url URL`
    Specify the URL to search for. If not provided, the script will prompt for input.

`-o, --open`
    Open successful results in the default web browser.

`-j, --json`
    Output results in JSON format.

# USAGE

1. Ensure you have Python 3 installed on your system.
2. Install the required library:
   ```
   pip install requests
   ```
3. Run the script with desired options:
   ```
   ./cache-me-outside.py [-u URL] [-o] [-j]
   ```

# OUTPUT

The script will display results for each service, showing either a link to the search results/cached page or a message indicating that no results were found. If the `-o` option is used, it will also open successful results in your default web browser.

# EXAMPLES

Search for a specific URL:
```
$ ./cache-me-outside.py -u https://example.com
```

Search for a URL and open results in the browser:
```
$ ./cache-me-outside.py -u https://example.com -o
```

Output results in JSON format:
```
$ ./cache-me-outside.py -u https://example.com -j
```

# NOTES

- This script provides links to search results or cached pages. It does not scrape or display the actual content of the pages.
- Some services might have restrictions on automated access. Use this script responsibly and in accordance with each service's terms of use.
- The script's effectiveness depends on the availability and indexing of content by the searched services.
- A small delay is added between requests to be respectful to the services being queried.

# LICENSE

MIT License

Copyright (c) 2024 inforensics.ai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# DISCLAIMER

This tool is for educational purposes only. Always respect privacy and adhere to the terms of service of the platforms you're querying. The authors and contributors are not responsible for any misuse or damage caused by this program.

# SEE ALSO

- Python Requests library documentation: https://docs.python-requests.org/
- Internet Archive: https://archive.org/
- Wayback Machine: https://web.archive.org/

# AUTHOR

This script and man page were created by inforensics.ai.

# BUGS

Please report any bugs or issues to the script maintainer at inforensics.ai.
