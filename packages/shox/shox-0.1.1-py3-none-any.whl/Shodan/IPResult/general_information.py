from bs4 import BeautifulSoup

class GeneralInformation:
    def __init__(self, soup):
        self.container = self._scrape_gi(soup)
        self.hostnames = self._scrape_hostnames(self.container)
        # self.domains = self._scrape_domains(self.containter) 
        # self.country = self._scrape_country(self.containter) 
        # self.organization = self._scrape_org(self.containter)
        # self.isp = self._scrape_isp(self.containter)
        # self.asn = self._scrape_asn(self.containter) 
        # self.last_seen = self._scrape_last_seen(self.containter)
        # self.tags = self._scrape_tags(self.containter)
    
    def _scrape_gi(self, soup):
        return soup.find('div', class_='card card-yellow card-padding')

    def _scrape_hostnames(self, container):
        print(container)
        
