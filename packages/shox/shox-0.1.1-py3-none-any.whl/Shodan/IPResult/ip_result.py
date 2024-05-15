from .general_information import GeneralInformation
from .web_technologies import WebTechnologies
from .open_ports import OpenPorts
from .vulnerabilities import Vulnerability
from .vulnerabilities import Vulnerabilities 

class IpResult:
    def __init__(self, soup):
        self.general_information = GeneralInformation(soup) 
        # self.open_ports = OpenPorts(soup) 
        # self.web_technologies = WebTechnologies(soup) 
        self.vulnerabilities = Vulnerabilities(soup) 
