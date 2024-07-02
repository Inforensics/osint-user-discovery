# Inforensics - OSINT User Discovery

![Inforensics](https://github.com/Inforensics/.github/blob/main/logo.png)

OSINT User Discovery is a set of Python scripts designed to search for users across different decentralized social media platforms. Currently, it supports searching for users on Nostr and Mastodon networks.

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

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/inforensics-ai/osint-user-discovery.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
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

For bug reports and feature requests, please open an issue on this repository
