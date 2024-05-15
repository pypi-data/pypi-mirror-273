from bs4 import BeautifulSoup

class Vulnerability:
    def __init__(self, cve_code, description, scoring='Unknown score'):
        self.cve_code = cve_code 
        self.description = description 
        self.scoring = scoring 

class Vulnerabilities:
    def __init__(self, soup):
        self.container = self._scrape_vulns_container(soup)
        self.table = self._scrape_vulns_table(self.container)
        self.arr_vulns = self._scrape_vulns(self.table)
        self.arr_cve_codes = self._get_cve_codes(self.arr_vulns)

    def _scrape_vulns_container(self, soup):
        return soup.find('div', class_='card card-red card-padding')

    def _scrape_vulns_table(self, container):
        try:
            table = container.find('table', id='vulnerabilities')
            if table:
                return table
            else:
                print("Table not found")
        except Exception as e:
            print("Exception: ", e)

    def _scrape_vulns(self, table):
        arr_vulns = []
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                cve_code = cells[0].text.strip()
                spans = cells[1].find_all('span')
                if len(spans) == 2:
                    scoring_span = cells[1].find('span', class_='tag')
                    description_span = cells[1].find('span', class_=False)
                    scoring = scoring_span.text.strip() if scoring_span else None
                    description = description_span.text.strip() if description_span else None
                else:
                    description = cells[1].text.strip()
                    scoring = "Unknown Scoring"

                vulnerability_obj = Vulnerability(cve_code, description, scoring)
                arr_vulns.append(vulnerability_obj)
        return arr_vulns

    def _get_cve_codes(self, arr_vulns):
        arr_cve_codes = []
        for vuln_obj in arr_vulns:
            arr_cve_codes.append(vuln_obj.cve_code)
        return arr_cve_codes

    # TODO: remove, this is for debugging
    def _print_arr_vulns(self, arr_vulns):
        count = 1
        for vuln_obj in arr_vulns:
            print("CVE Code: ", vuln_obj.cve_code)
            print("description: ", vuln_obj.description)
            print("scoring: ", vuln_obj.scoring)
            print("-" * 30, count)
            count += 1


    # TODO: remove, this is for debugging
    def _print_arr(self, arr):
        for entry in arr:
            print(entry)
            print("-" * 30)
