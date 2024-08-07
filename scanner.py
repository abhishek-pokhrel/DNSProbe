import argparse
import logging
import dns.resolver
from logging.handlers import RotatingFileHandler
from typing import List
import time
from tabulate import tabulate
import threading
import queue
import yaml
from colorama import init, Fore, Style

# list of all common DNS record types / default list
DEFAULT_RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]

def load_config(config_file: str) -> dict:
    """
    Load configuration from a YAML file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration data.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def setup_logging(config: dict) -> None:
    """
    Set up logging configuration with rotating file handler and detailed format.

    Args:
        config (dict): Configuration data.
    """
    log_level = getattr(logging, config.get('log_level', 'INFO'))
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Create rotating file handler
    handler = RotatingFileHandler('dns_scanner.log', maxBytes=5*1024*1024, backupCount=3)
    handler.setLevel(log_level)
    
    # formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - Line %(lineno)d - %(message)s')
    
    # adding handler to formatter
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)

    # log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def perform_dns_lookup(target_domain: str, record_type: str, results: queue.Queue, resolver: dns.resolver.Resolver) -> None:
    """
    Perform DNS lookup for the specified domain and record type.

    Args:
        target_domain (str): The domain to query.
        record_type (str): The DNS record type to query.
        results (queue.Queue): The queue to store results.
        resolver (dns.resolver.Resolver): The DNS resolver to use.
    """
    logger = logging.getLogger(__name__)
    start_time = time.time()
    try:
        answers = resolver.resolve(target_domain, record_type)
        end_time = time.time()
        query_time = end_time - start_time

        for rdata in answers:
            results.put({
                "Host": target_domain,
                "Record Type": record_type,
                "Result": str(rdata),
                "Time Taken (s)": f"{query_time:.4f}"
            })
        logger.info(f"{record_type} records for {target_domain}: {answers}")
    except dns.resolver.NoAnswer:
        logger.warning(f"No {record_type} records found for {target_domain}")
    except dns.resolver.NXDOMAIN:
        logger.error(f"Domain {target_domain} does not exist")
    except Exception as e:
        logger.error(f"Error resolving {record_type} records for {target_domain}: {e}")

def colorize_result(result: dict) -> dict:
    """
    Add color to the result dictionary for console output.

    Args:
        result (dict): The result dictionary.

    Returns:
        dict: The colorized result dictionary.
    """
    colorized_result = result.copy()
    colorized_result["Host"] = Fore.YELLOW + result["Host"] + Style.RESET_ALL
    colorized_result["Record Type"] = Fore.CYAN + result["Record Type"] + Style.RESET_ALL
    colorized_result["Result"] = Fore.GREEN + result["Result"] + Style.RESET_ALL
    colorized_result["Time Taken (s)"] = Fore.MAGENTA + result["Time Taken (s)"] + Style.RESET_ALL
    return colorized_result

def main() -> None:
    """
    Main function to parse arguments and initiate DNS lookup.
    """
    # Initialize colorama
    init(autoreset=True)

    # Load configuration
    config = load_config('config.yaml')
    setup_logging(config)

    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description="DNSProbe")
    parser.add_argument("domain", type=str, help="The target domain to scan")
    parser.add_argument("--version", action="version", version="DNSProbe 1.0")
    
    args = parser.parse_args()

    logger.info(f"Starting DNS scan for domain: {args.domain}")

    # Set up DNS resolver
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [config.get('dns_server', '8.8.8.8')]
    record_types = config.get('record_types', DEFAULT_RECORD_TYPES)

    results = queue.Queue()
    threads = []

    for record_type in record_types:
        thread = threading.Thread(target=perform_dns_lookup, args=(args.domain, record_type, results, resolver))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    results_list = []
    while not results.empty():
        results_list.append(results.get())

    if results_list:
        colorized_results = [colorize_result(result) for result in results_list]
        print(tabulate(colorized_results, headers="keys", tablefmt="grid"))

    logger.info("DNS scan completed")

if __name__ == "__main__":
    main()