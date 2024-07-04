# Inforensics - OSINT User Discovery
![Inforensics](https://github.com/Inforensics/.github/blob/main/logo.png)  
OSINT Discovery is a set of Python scripts designed to search for users or URLs across different social media platforms and caching services. Currently, it supports searching for users on Nostr and Mastodon networks, searching for cached tweets across various archiving services, and searching for cached versions of any URL.
Created by [inforensics.ai](https://inforensics.ai)

## Scripts

### 1. Nostr User Search
This script searches for a Nostr user across multiple relays.
#### Features:
- Search by public key or NIP-05 identifier
- Use default relays or specify custom ones
- Read relay list from a file
- Verbose mode for detailed output
#### Usage:
```
python nostr-user-search.py [-h] [-r RELAYS [RELAYS ...]] [-f FILE] [-v] identifier
```

### 2. Mastodon User Search
This script searches for a Mastodon user across multiple instances.
#### Features:
- Fetch instances from the instances.social API
- Specify custom instances or read from a file
- Control minimum instance size and status
- Verbose mode for detailed output
#### Usage:
```
python mastodon-user-search.py [-h] [-c COUNT] [-m MIN_USERS] [--include-down] [--include-closed] [-v] [-i INSTANCES [INSTANCES ...]] [-f FILE] username
```

### 3. Tweet Cache Search
This script searches for cached tweets of a specified Twitter username across multiple archiving and caching services.
#### Features:
- Search across multiple caching services (Wayback Machine, Google Cache, etc.)
- Option to open results in the default web browser
- Command-line interface with optional arguments
#### Usage:
```
python tweet-cache-search.py [-h] [-u USERNAME] [-o]
```

### 4. Cache-Me-Outside
This script searches for cached versions of any URL across various caching and archiving services.
#### Features:
- Search across multiple services (Wayback Machine, Google Cache, Bing, Yandex, etc.)
- Option to open results in the default web browser
- JSON output option for easy parsing
- Automatic installation of required libraries
#### Usage:
```
python cache-me-outside.py [-h] [-u URL] [-o] [-j]
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/inforensics-ai/osint-user-discovery.git
   ```
2. Navigate to the project directory:
   ```
   cd osint-user-discovery
   ```
3. Each script will attempt to install its required dependencies when run. However, you can also install all dependencies manually:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - For the Mastodon script, you need an API key from instances.social. Create a `.env` file in the project root and add:
     ```
     INSTANCES_API_KEY=your_api_key_here
     ```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer
This tool is for educational and research purposes only. Always respect privacy and adhere to the terms of service of the platforms you're querying.

## Contact
For bug reports and feature requests, please open an issue on this repository.
