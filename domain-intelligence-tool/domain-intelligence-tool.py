#!/usr/bin/env python3

import sys
import json
import argparse
import os
from pathlib import Path
import dns.resolver
import socket
import ssl
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import whois
from ipwhois import IPWhois
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import subprocess
import re
from tqdm import tqdm
import dns.zone
import geoip2.database
import OpenSSL
import idna

ASCII_BANNER = '''
██╗███╗   ██╗███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗███████╗██╗ ██████╗███████╗
██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██║██╔════╝██╔════╝
██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║███████╗██║██║     ███████╗
██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║╚════██║██║██║     ╚════██║
██║██║ ╚████║██║     ╚██████╔╝██║  ██║███████╗██║ ╚████║███████║██║╚██████╗███████║
╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝╚══════╝

                        Domain Intelligence Tool
'''

# Load configuration
def load_config(config_path):
    default_config = {
        "api_keys": {
            "geoip2": ""
        },
        "markdown_output_path": "",
        "geolite2_db_path": "GeoLite2-City.mmdb"
    }
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        # Update default config with loaded config
        default_config.update(config)
    else:
        print(f"Config file not found at {config_path}. Using default configuration.")
    
    return default_config

# Global configuration variable
CONFIG = load_config('config.json')

def is_website_live(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=10)
        response.raise_for_status()
        return True
    except RequestException:
        try:
            response = requests.get(f"https://{domain}", timeout=10)
            response.raise_for_status()
            return True
        except RequestException:
            return False

def get_dns_records(domain):
    dns_info = {}
    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA', 'SRV']
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            dns_info[record_type] = [str(rdata) for rdata in answers]
        except dns.resolver.NoAnswer:
            dns_info[record_type] = []
        except dns.resolver.NXDOMAIN:
            dns_info[record_type] = "Domain does not exist"
        except Exception as e:
            dns_info[record_type] = f"Error: {str(e)}"
    
    return dns_info

def get_ssl_info(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                der_cert = secure_sock.getpeercert(binary_form=True)
                cert = x509.load_der_x509_certificate(der_cert, default_backend())
                
                cert_info = {
                    "subject": ", ".join([f"{attr.oid._name}={attr.value}" for attr in cert.subject]),
                    "issuer": ", ".join([f"{attr.oid._name}={attr.value}" for attr in cert.issuer]),
                    "version": cert.version.name,
                    "serialNumber": cert.serial_number,
                    "notBefore": cert.not_valid_before_utc,
                    "notAfter": cert.not_valid_after_utc,
                    "subjectAltName": [
                        f"{name.value}" for name in cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME).value
                    ] if cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME) else [],
                }
                
                return cert_info
    except ssl.SSLError as e:
        return f"SSL Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": w.creation_date,
            "expiration_date": w.expiration_date,
            "name_servers": w.name_servers
        }
    except Exception as e:
        return f"WHOIS Error: {str(e)}"

def get_ip_info(ip):
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        return {
            "ASN": results.get('asn'),
            "ASN_Country": results.get('asn_country_code'),
            "ASN_Description": results.get('asn_description')
        }
    except Exception as e:
        return f"IP WHOIS Error: {str(e)}"

def detect_web_technologies(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        technologies = []
        if 'wordpress' in response.text.lower():
            technologies.append('WordPress')
        if 'joomla' in response.text.lower():
            technologies.append('Joomla')
        if 'drupal' in response.text.lower():
            technologies.append('Drupal')
        
        server = response.headers.get('Server')
        if server:
            technologies.append(f"Web Server: {server}")
        
        return technologies
    except Exception as e:
        return f"Web Technology Detection Error: {str(e)}"

def enumerate_subdomains(domain):
    try:
        output = subprocess.check_output(['sublist3r', '-d', domain, '-o', 'subdomains.txt'], stderr=subprocess.STDOUT)
        with open('subdomains.txt', 'r') as f:
            subdomains = f.read().splitlines()
        subprocess.run(['rm', 'subdomains.txt'])
        return subdomains
    except Exception as e:
        return f"Subdomain Enumeration Error: {str(e)}"

def check_ssl_vulnerabilities(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                cipher = secure_sock.cipher()
                version = secure_sock.version()
                
        return {
            "SSL Version": version,
            "Cipher Suite": cipher[0],
            "Bit Strength": cipher[2],
        }
    except ssl.SSLError as e:
        return f"SSL Vulnerability Check Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_http_headers(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        return dict(response.headers)
    except Exception as e:
        return f"HTTP Headers Analysis Error: {str(e)}"

def check_email_security(domain):
    try:
        dmarc = dns.resolver.resolve(f"_dmarc.{domain}", 'TXT')
        spf = dns.resolver.resolve(domain, 'TXT')
        return {
            "DMARC": str(dmarc[0]),
            "SPF": str(spf[0])
        }
    except dns.resolver.NXDOMAIN:
        return {
            "DMARC": "Not found",
            "SPF": "Not found"
        }
    except Exception as e:
        return {
            "Error": f"Email Security Check Error: {str(e)}"
        }

def get_caa_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'CAA')
        return [str(rdata) for rdata in answers]
    except Exception as e:
        return f"CAA Record Error: {str(e)}"

def get_tlsa_records(domain):
    try:
        answers = dns.resolver.resolve(f"_443._tcp.{domain}", 'TLSA')
        return [str(rdata) for rdata in answers]
    except Exception as e:
        return f"TLSA Record Error: {str(e)}"

def get_reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception as e:
        return f"Reverse DNS Error: {str(e)}"

def get_domain_age(creation_date):
    if creation_date:
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = datetime.now() - creation_date
        return f"{age.days} days"
    return "Unknown"

def get_ssl_cert_chain(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                der_cert = secure_sock.getpeercert(binary_form=True)
                cert = x509.load_der_x509_certificate(der_cert, default_backend())
                
                chain = []
                current_cert = cert
                while current_cert:
                    cert_info = {
                        "subject": ", ".join([f"{attr.oid._name}={attr.value}" for attr in current_cert.subject]),
                        "issuer": ", ".join([f"{attr.oid._name}={attr.value}" for attr in current_cert.issuer]),
                        "not_before": current_cert.not_valid_before_utc,
                        "not_after": current_cert.not_valid_after_utc,
                    }
                    chain.append(cert_info)
                    
                    # If the issuer is the same as the subject, we've reached the root certificate
                    if current_cert.subject == current_cert.issuer:
                        break
                    
                    # Try to fetch the next certificate in the chain
                    try:
                        issuer_cert = fetch_issuer_cert(current_cert)
                        if issuer_cert:
                            current_cert = issuer_cert
                        else:
                            break
                    except Exception:
                        break
                
                return chain
    except ssl.SSLError as e:
        return f"SSL Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def fetch_issuer_cert(cert):
    # This is a placeholder function. In a real-world scenario, you would implement
    # logic to fetch the issuer's certificate, possibly from a certificate store or online.
    # For now, we'll just return None to indicate we can't fetch further certificates.
    return None

def get_security_headers(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        security_headers = {
            'Strict-Transport-Security': response.headers.get('Strict-Transport-Security', 'Not Set'),
            'Content-Security-Policy': response.headers.get('Content-Security-Policy', 'Not Set'),
            'X-Frame-Options': response.headers.get('X-Frame-Options', 'Not Set'),
            'X-XSS-Protection': response.headers.get('X-XSS-Protection', 'Not Set'),
            'X-Content-Type-Options': response.headers.get('X-Content-Type-Options', 'Not Set'),
            'Referrer-Policy': response.headers.get('Referrer-Policy', 'Not Set'),
            'Feature-Policy': response.headers.get('Feature-Policy', 'Not Set'),
        }
        return security_headers
    except Exception as e:
        return f"Security Headers Error: {str(e)}"

def get_web_server_version(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        server = response.headers.get('Server', 'Not Disclosed')
        return server
    except Exception as e:
        return f"Web Server Version Error: {str(e)}"

def check_dnssec(domain):
    try:
        answers = dns.resolver.resolve(domain, 'DNSKEY')
        return "DNSSEC is implemented"
    except dns.resolver.NoAnswer:
        return "DNSSEC is not implemented"
    except Exception as e:
        return f"DNSSEC Check Error: {str(e)}"

def get_ip_geolocation(ip):
    try:
        with geoip2.database.Reader(CONFIG['geolite2_db_path']) as reader:
            response = reader.city(ip)
            return {
                'country': response.country.name,
                'city': response.city.name,
                'latitude': response.location.latitude,
                'longitude': response.location.longitude,
            }
    except Exception as e:
        return f"IP Geolocation Error: {str(e)}"

def check_ssl_tls_protocols(domain):
    protocols = ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
    supported = {}
    for protocol in protocols:
        try:
            context = ssl.create_default_context()
            context.set_ciphers('ALL:@SECLEVEL=0')
            context.minimum_version = getattr(ssl, f'{protocol.replace(".", "_")}_METHOD')
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                    supported[protocol] = True
        except:
            supported[protocol] = False
    return supported

def check_domain_reputation(domain):
    blacklists = [
        'zen.spamhaus.org',
        'bl.spamcop.net',
        'cbl.abuseat.org',
    ]
    results = {}
    for bl in blacklists:
        try:
            host = f"{domain}.{bl}"
            socket.gethostbyname(host)
            results[bl] = "Listed"
        except:
            results[bl] = "Not Listed"
    return results

def get_robots_txt(domain):
    try:
        response = requests.get(f"https://{domain}/robots.txt", timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            return f"No robots.txt found (Status code: {response.status_code})"
    except Exception as e:
        return f"Robots.txt Error: {str(e)}"

def get_sitemap(domain):
    try:
        response = requests.get(f"https://{domain}/sitemap.xml", timeout=5)
        if response.status_code == 200:
            return "Sitemap found"
        else:
            return f"No sitemap.xml found (Status code: {response.status_code})"
    except Exception as e:
        return f"Sitemap Error: {str(e)}"

def check_dns_propagation(domain):
    nameservers = [
        '8.8.8.8', '1.1.1.1', '9.9.9.9', '208.67.222.222',
        '8.8.4.4', '1.0.0.1', '149.112.112.112', '208.67.220.220'
    ]
    results = {}
    for ns in nameservers:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [ns]
            answers = resolver.resolve(domain, 'A')
            results[ns] = [str(rdata) for rdata in answers]
        except Exception as e:
            results[ns] = f"Error: {str(e)}"
    return results

def check_hsts_preload(domain):
    try:
        response = requests.get(f"https://hstspreload.org/api/v2/status/{domain}", timeout=5)
        
        if response.status_code == 404:
            return "Domain not found in HSTS preload list"
        
        response.raise_for_status()
        data = response.json()
        return data.get('status', 'Status not found in response')
    
    except requests.RequestException as e:
        return f"HSTS Preload Check Error: {str(e)}"
    except json.JSONDecodeError as json_err:
        return f"JSON Parsing Error: {str(json_err)}. Raw response: {response.text[:100]}..."

def generate_domain_variations(domain):
    variations = set()  # Using a set to avoid duplicates
    parts = domain.split('.')
    name = parts[0]
    tld = '.'.join(parts[1:])

    # Common TLD variations
    variations.add(f"{name}.co")
    variations.add(f"{name}.org")
    variations.add(f"{name}.net")

    # Hyphen variation
    variations.add(f"{name}-{tld}")

    # Number substitutions
    variations.add(name.replace('i', '1') + '.' + tld)
    variations.add(name.replace('l', '1') + '.' + tld)
    variations.add(name.replace('o', '0') + '.' + tld)
    variations.add(name + '.' + tld.replace('o', '0'))

    # Character swaps
    for i in range(len(name) - 1):
        swapped = list(name)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variations.add(''.join(swapped) + '.' + tld)

    # Remove the original domain if it's in the set
    variations.discard(domain)

    return list(variations)

def attempt_zone_transfer(domain):
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        nameservers = [str(rdata) for rdata in answers]
        
        for ns in nameservers:
            try:
                z = dns.zone.from_xfr(dns.query.xfr(ns, domain))
                return {str(name): str(z[name].to_text()) for name in z.nodes.keys()}
            except Exception as e:
                pass
        return "Zone transfer not allowed"
    except Exception as e:
        return f"Zone Transfer Error: {str(e)}"

def main(domain, json_output=False, markdown_output=False):
    print(ASCII_BANNER)
    print(f"Analyzing domain: {domain}\n")

    result = {
        "domain": domain,
        "query_time": datetime.now().isoformat(),
    }

    # Check if the website is live
    if not is_website_live(domain):
        result["status"] = "Domain does not have a live website"
        result["error"] = "Unable to connect to the website. The domain might not be hosted or could be blocking our requests."
        
        if json_output:
            print(json.dumps(result, indent=2, default=str))
        elif markdown_output:
            output_path = CONFIG['markdown_output_path'] or os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(output_path, f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            with open(filename, 'w') as f:
                f.write(f"# Inforensics Domain Intelligence Report for {domain}\n\n")
                f.write(f"Query Time: {result['query_time']}\n\n")
                f.write(f"## Status\n\n{result['status']}\n\n")
                f.write(f"## Error\n\n{result['error']}\n\n")
                f.write("\n---\n")
                f.write("Generated by Inforensics Domain Intelligence Tool\n")
                f.write("Created by [Inforensics](https://inforensics.ai)\n")
            print(f"Markdown report saved as {filename}")
        else:
            print(f"\nStatus: {result['status']}")
            print(f"Error: {result['error']}")
        
        return

    tasks = [
        ("DNS Records", get_dns_records),
        ("SSL Certificate", get_ssl_info),
        ("WHOIS Information", get_whois_info),
        ("Web Technologies", detect_web_technologies),
        ("Subdomains", enumerate_subdomains),
        ("SSL Vulnerabilities", check_ssl_vulnerabilities),
        ("HTTP Headers", analyze_http_headers),
        ("Email Security", check_email_security),
        ("CAA Records", get_caa_records),
        ("TLSA Records", get_tlsa_records),
        ("SSL Certificate Chain", get_ssl_cert_chain),
        ("Security Headers", get_security_headers),
        ("Web Server Version", get_web_server_version),
        ("DNSSEC", check_dnssec),
        ("SSL/TLS Protocols", check_ssl_tls_protocols),
        ("Domain Reputation", check_domain_reputation),
        ("Robots.txt", get_robots_txt),
        ("Sitemap", get_sitemap),
        ("DNS Propagation", check_dns_propagation),
        ("HSTS Preload Status", check_hsts_preload),
        ("Domain Variations", generate_domain_variations),
        ("Zone Transfer", attempt_zone_transfer),
    ]

    with tqdm(total=len(tasks), desc="Progress", unit="task") as pbar:
        for task_name, task_func in tasks:
            result[task_name] = task_func(domain)
            pbar.update(1)

    # Get IP info and Reverse DNS for each A record
    result["IP Info"] = {}
    result["Reverse DNS"] = {}
    a_records = result.get("DNS Records", {}).get('A', [])
    with tqdm(total=len(a_records), desc="IP Info", unit="ip") as pbar:
        for ip in a_records:
            result['IP Info'][ip] = get_ip_info(ip)
            result['Reverse DNS'][ip] = get_reverse_dns(ip)
            pbar.update(1)

    # Get IP Geolocation
    result["IP Geolocation"] = {}
    with tqdm(total=len(a_records), desc="IP Geolocation", unit="ip") as pbar:
        for ip in a_records:
            result['IP Geolocation'][ip] = get_ip_geolocation(ip)
            pbar.update(1)

    # Calculate Domain Age
    if isinstance(result.get('WHOIS Information'), dict) and 'creation_date' in result['WHOIS Information']:
        result['Domain Age'] = get_domain_age(result['WHOIS Information']['creation_date'])
    else:
        result['Domain Age'] = "Unable to calculate (WHOIS information not available)"

    if json_output:
        print(json.dumps(result, indent=2, default=str))
    elif markdown_output:
        output_path = CONFIG['markdown_output_path'] or os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(output_path, f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        with open(filename, 'w') as f:
            f.write(f"# Inforensics Domain Intelligence Report for {domain}\n\n")
            f.write(f"Query Time: {result['query_time']}\n\n")
            
            for key, value in result.items():
                if key not in ['domain', 'query_time']:
                    f.write(f"## {key}\n\n")
                    f.write(f"```\n{json.dumps(value, indent=2, default=str)}\n```\n\n")
            
            f.write("\n---\n")
            f.write("Generated by Inforensics Domain Intelligence Tool\n")
            f.write("Created by [Inforensics](https://inforensics.ai)\n")
        print(f"Markdown report saved as {filename}")
    else:
        print(f"\nInforensics Domain Intelligence Report for {domain}")
        print(f"Query Time: {result['query_time']}")
        for key, value in result.items():
            if key not in ['domain', 'query_time']:
                print(f"\n{key}:")
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, list):
                            print(f"  {subkey}:")
                            for item in subvalue:
                                print(f"    {item}")
                        else:
                            print(f"  {subkey}: {subvalue}")
                elif isinstance(value, list):
                    for item in value:
                        print(f"  {item}")
                else:
                    print(f"  {value}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inforensics Domain Intelligence Tool")
    parser.add_argument("domain", help="The domain to query")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--markdown", action="store_true", help="Output in Markdown format")
    parser.add_argument("--config", default="config.json", help="Path to configuration file")
    args = parser.parse_args()

    CONFIG = load_config(args.config)
    main(args.domain, args.json, args.markdown)
