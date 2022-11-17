#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from ipaddress import IPv4Address, ip_address, ip_network

try:
    from loguru import logger
except ImportError:
    print("ERROR: Please pip install loguru")
    sys.exit(1)


def parse_args():
    """
    Parses debug and folder arguments.

    Variables:
    debug (bool): If True, debug logging will be enabled. Default = False
    ip (str): IP Address to search for. Required.

    Returns: (argparse.Namespace): Parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        required=False,
        help="Enable debug logging",
    )
    parser.add_argument("ip", help="IPv4 Address to search")
    return parser.parse_args()


def setup_logging(debug: bool):
    """
    Setup loguru logging.

    Variables:
    debug (bool): If True, debug logging will be enabled. Default = False

    Returns:
    logger (loguru.logger): Loguru logger object.
    """
    # Remove all built in handlers
    logger.remove()
    # Set custom loguru format
    fmt = (
        "<level>{time:YYYY-MM-DD hh:mm:ss A}</level> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{"
        "function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> "
    )
    # Set Debug level if --debug is passed
    if debug:
        logger.add(sys.stderr, format=fmt, level="DEBUG")
    else:
        logger.add(sys.stderr, format=fmt, level="WARNING")
    return logger


def load_networks(file):
    """
    Loads ./networks.csv file, uses header as keys, and creates a list of dicts.

    Returns:
    networks (list of dict): Collection of networks from file. Each network is a dict.
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    collected_networks = []
    logger.debug(f"Loading {file}")
    try:
        with open(file, "r") as f:
            header = f.readline().strip().split(",")
            logger.debug(f"Headers: {header}")
            for line in f:
                values = line.strip().split(",")
                collected_networks.append(dict(zip(header, values)))
        logger.debug(f"Found {len(collected_networks)} networks")
        return collected_networks
    except FileNotFoundError:
        logger.error(f"Could not find {file}")
        sys.exit(1)


def convert_to_ip_address(input_ip) -> IPv4Address:
    """
    Validates if IP address is valid.

    Returns:
    ip_address (ipaddress.IPv4Address): IP Address object.
    """
    try:
        return ip_address(input_ip)
    except ValueError:
        logger.error(f"{input_ip} is not a valid IP Address")
        sys.exit(1)


def search_networks(search_ip, sourced_networks):
    for network in sourced_networks:
        if search_ip in ip_network(network["CIDR"]):
            logger.success(f"Found {search_ip} in {network['CIDR']}")
            print(
                f"{search_ip} found in {network['CIDR']} - {network['Description']}"
            )
            return network
    logger.error(f"Could not find {search_ip} in any networks")


if __name__ == "__main__":
    # Parse the arguments
    args = parse_args()
    # setup logger
    logger = setup_logging(args.debug)

    ip = args.ip
    ip = convert_to_ip_address(ip)
    networks = load_networks("networks.csv")
    search_networks(ip, networks)
