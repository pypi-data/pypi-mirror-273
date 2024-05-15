import re
import socket
import dns.resolver
import requests
from bs4 import BeautifulSoup

""" from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys """


# dns lookup
def dns_lookup(domainname):
    try:
        results = dns.resolver.resolve(domainname, "A")
        counter = 1
        for val in results:
            print(f"Address record [{counter}]: ", val.to_text())
            counter += 1
    except dns.resolver.NoAnswer:
        print(f"Error: No A Records found for {domainname}.")
    except dns.resolver.NXDOMAIN:
        print(f"Error: Domain {domainname} does not exist.")
    except dns.exception.Timeout:
        print(f'Error: DNS resolution for "{domainname}" timed out.')
    except dns.resolver.ResolverError:
        print(f"Error: Resolver Error occurred for {domainname}.")


# validate ipv4-address input
def validate_ipv4(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False


# validate domain name input
def validate_domainname(domainname):
    domain_reg = r"^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$"
    return bool(re.match(domain_reg, domainname))


# check for /host/<ip>, returns html upon success, raises error otherwise
def get_html(ip):
    url = f"https://www.shodan.io/host/{ip}"
    try:
        response = requests.get(url, headers={"User-Agent": "curl/7.0"})
        # Raise error for responses other than 200
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print("Page not found")
        elif e.response.status_code == 403:
            print("Forbidden access")
        else:
            print("Status code: ", e.response.status_code)
    except requests.RequestException as e:
        print("Error:", e)


""" def get_ipv4_soup(ipv4_addr):
    driver = webdriver.Chrome()
    driver.get(f"https://www.shodan.io/host/{ipv4_addr}")
    page_source = driver.page_source
    driver.quit()
    return BeautifulSoup(page_source, 'html.parser') """
