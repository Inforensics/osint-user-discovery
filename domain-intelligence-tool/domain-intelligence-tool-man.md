# Inforensics Domain Intelligence Tool

## Overview

The Inforensics Domain Intelligence Tool is a comprehensive Python script designed for gathering and analyzing various aspects of domain information. It provides a wide range of checks and analyses, making it a valuable tool for cybersecurity professionals, system administrators, and researchers.

## Features

- DNS record retrieval (A, AAAA, CNAME, MX, NS, TXT, SOA, SRV)
- SSL/TLS certificate analysis
- WHOIS information retrieval
- Web technology detection
- Subdomain enumeration
- SSL/TLS vulnerability checks
- HTTP header analysis
- Email security configuration (DMARC, SPF)
- CAA and TLSA record checks
- Reverse DNS lookups
- Domain age calculation
- SSL certificate chain analysis
- Security header checks
- Web server version detection
- DNSSEC implementation check
- IP geolocation
- SSL/TLS protocol support check
- Domain reputation check (against common blacklists)
- Robots.txt and sitemap.xml retrieval
- DNS propagation check
- HSTS preload status check
- Generation of common domain variations
- DNS zone transfer attempt

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/inforensics/domain-intelligence-tool.git
   cd domain-intelligence-tool
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Download the GeoLite2-City.mmdb database and place it in the location specified in your config.json file.

4. Create a `config.json` file in the same directory as the script (see Configuration section below).

## Usage

Basic usage:
```
python inforensics_domain_intelligence.py example.com
```

Output in JSON format:
```
python inforensics_domain_intelligence.py example.com --json
```

Output in Markdown format:
```
python inforensics_domain_intelligence.py example.com --markdown
```

Use a custom configuration file:
```
python inforensics_domain_intelligence.py example.com --config custom_config.json
```

## Configuration

Create a `config.json` file with the following structure:

```json
{
    "api_keys": {
        "geoip2": "your_geoip2_api_key_here"
    },
    "markdown_output_path": "/path/to/output/directory",
    "geolite2_db_path": "/path/to/GeoLite2-City.mmdb"
}
```

## Output

The tool provides output in three formats:
1. Console output (default)
2. JSON format (use `--json` flag)
3. Markdown format (use `--markdown` flag)

## Caution

This tool performs active reconnaissance on the specified domain. Ensure you have permission to scan the target domain before use. Some features (like subdomain enumeration) may be intrusive and should be used with caution.

## Contributing

Contributions to the Inforensics Domain Intelligence Tool are welcome! Please feel free to submit pull requests, create issues or spread the word.

## License

This project is licensed under MIT [LICENSE](../LICENSE) file for details.

## Disclaimer

This tool is for educational and ethical use only. Always obtain proper authorization before scanning any domains you do not own or have explicit permission to test.

## Contact

For bugs, questions, and discussions please use the [GitHub Issues](https://github.com/inforensics/domain-intelligence-tool/issues).

## Acknowledgments

- Thanks to all the open-source projects that made this tool possible.
- Special thanks to the Inforensics team for their continuous support and contributions.

