#!/usr/bin/python3

import requests
import sys


def send_payloads(target, payloads):
    found = 0
    failed = []
    for payload in payloads:
        try:
            code = requests.get(f"{target}/{payload}").status_code
            if code >= 500 or code < 400 or code == 401 or code == 403 or code == 451:
                color = ''
                if 300 > code >= 200:
                    color = Colors.OKBLUE
                elif code >= 500 or code == 401 or code == 403 or code == 451:
                    color = Colors.WARNING
                elif code < 200:
                    color = Colors.OKCYAN

                print(f"{color}{code}{Colors.RESET} ::: {target}/{payload.strip()}")
                found += 1
        except:
            failed.append(payload)

    return found, failed


class Colors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def brute(target, dictionary_directory):
    try:
        with open(dictionary_directory, "r") as file:
            payloads = file.readlines()
    except:
        print(f"{Colors.FAIL}Could not handle the given dictionary{Colors.RESET}")
        return

    try:
        test = requests.get(target)
    except:
        print(f"{Colors.FAIL}Could not handle the given target{Colors.RESET}")
        return

    found = 0
    first_try = send_payloads(target, payloads)
    found += first_try[0]

    if len(first_try[1]) > 0:
        try_again = input(f"Failed to connect to {first_try[0]} directories, want to try again? (y/N)")
        if try_again.lower() == 'y':
            found += send_payloads(target, first_try[1])[0]

    try_recursively = input("Want to try recursively? (y/N)")
    if try_recursively.lower() == 'y':
        for directory in payloads:
            rec_found = send_payloads(f"{target}/{directory}", payloads)[0]

        found += rec_found
        print(f"Found {rec_found} directories recursively")

    print(f"Total of {Colors.OKCYAN}{found}{Colors.RESET} directories found")

if __name__ == "__main__":
    brute(str(sys.argv[1]), sys.argv[2])
