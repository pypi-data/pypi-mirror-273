import click
import dns.resolver                     # dns_lookup
import socket
import re                               # for validate_domainname(target)
import requests                         # for get_html(ip)
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from IPResult.ip_result import IpResult
from IPResult.general_information import GeneralInformation 
from IPResult.vulnerabilities import Vulnerabilities


# dns lookup
def dns_lookup(domainname):
    try:
        results = dns.resolver.resolve(domainname, 'A')
        counter = 1
        for val in results:
            print(f"Address record [{counter}]: ", val.to_text())
            counter += 1
    except dns.resolver.NoAnswer:
        print(f"Error: No A Records found for {domainname}.")
    except dns.resolver.NXDOMAIN:
        print(f"Error: Domain {domainname} does not exist.")
    except dns.exception.Timeout:
        print(f"Error: DNS resolution for \"{domainname}\" timed out.")
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
        response = requests.get(url)
        # Raise error for responses other than 200
        response.raise_for_status()
        return response.content
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print("Page not found")
        elif e.response.status_code == 403:
            print("Forbidden access")
        else:
            print("Status code: ", e.response.status_code)
    except requests.RequestException as e:
        print("Error:", e)


# ipv4 handling for shodan
def get_ipv4_shodan(ipv4_addr):
    driver = webdriver.Chrome()
    driver.get(f"https://www.shodan.io/host/{ipv4_addr}")
    page_source = driver.page_source
    driver.quit()
    return page_source



# click cli
@click.command()
@click.argument('target')  # target is either a ipv4-address or a domainname
def main(target):
    print(target)
    if validate_domainname(target):
        click.echo(f"results for: {target}")
        dns_lookup(target)
        # TODO: handle domainname
        print("TODO: handle domainname")
    elif validate_ipv4(target):
        # TODO: handle ipv4

        page_source = get_ipv4_shodan(target)        
        soup = BeautifulSoup(page_source, 'html.parser')

        # IPResult
        ip_result = IpResult(soup)

        # General Information
        gen_inf = ip_result.general_information 

        # Open Ports
        # ports_div = soup.find('div', class_='card card-light-blue card-padding')

        # Web Technologies
        # web_techs = ip_result.web_technologies

        # Vulnerabilities
        vulns = ip_result.vulnerabilities 
        # print(vulns.table)

               # print(ports_div)

        # TODO: generate ip-result object
    else:
        click.echo("Invalid input")
        # TODO: more verbose error handling


if __name__ == "__main__":
    main()
