#Imports
from bs4 import BeautifulSoup
import requests , re , random , os ,time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
import json
import logging
from datetime import datetime
from pathlib import Path

def create_header_file(header_file_path):
    data = {}
    data['user_agents_links'] = [
    'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/',
    'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/2',
    'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/linux/',
    'https://developers.whatismybrowser.com/useragents/explore/software_name/safari/',
    'https://developers.whatismybrowser.com/useragents/explore/software_name/opera/',
    'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/chrome-os/',
    'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/',
    'https://developers.whatismybrowser.com/useragents/explore/operating_platform_string/redmi/',
    'https://developers.whatismybrowser.com/useragents/explore/software_name/instagram/',
    'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/android/',
    'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/ios/',
    'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/mac-os-x/'
    ]
    data['referrer'] = [
        "https://duckduckgo.com/",
        "https://www.google.com/",
        "http://www.bing.com/",
        "https://in.yahoo.com/",
        "https://www.azlyrics.com/",
        "https://www.dogpile.com/",
        "http://www.yippy.com",
        "https://yandex.com/"
        ]
        
    data['user_agents_scrap'] = [
    
    ]
    data['proxies'] = []
    data['working_proxies'] = []
    
    with open(header_file_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
def file_exisits(file_path):
    path = Path(file_path)
    return path.is_file()
  
class Proxies:
    def __init__(self , data_file = 'data-header-details.json' , 
                pubproxy = 'http://pubproxy.com/api/proxy?port=8080,3128,3129,51200,8811,8089,33746,8880,32302,80,8118,8081',
                proxyscrape = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=elite' ,
                free_p_l = 'https://free-proxy-list.net/'):

        self.data_file = data_file  # To save Location of where you have saved Json File
        if not file_exisits(self.data_file):
            create_header_file(self.data_file)
        self.data = json.load(open(os.path.abspath(self.data_file) , 'r+'))
        self.pubproxy = pubproxy
        self.proxyscrape = proxyscrape
        self.free_p_l = free_p_l
        self.def_logger()
        
    def needToGetProxies(self):
        return self.data['proxies'] == [] or self.data['working_proxies'] == []
        #if either self.data['proxies'] or self.data['working_proxies'] is empty 
    
    # Definign Logger for this class
    def def_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s : %(filename)s : %(funcName)s : %(levelname)s : %(message)s')
        self.file_handler = logging.FileHandler(os.path.abspath('proxies.log'))
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
    
    # Function to return Header when called
    def return_header(self):
        header = {
                'user-agent':self.data['user_agents_scrap'][random.randint(0,len(self.data['user_agents_scrap'])-1)] , 
                'referer':self.data['referrer'][random.randint(0,len(self.data['referrer'])-1)],
                'Upgrade-Insecure-Requests': '0' , 
                'DNT':'1' , 
                'Connection':'keep-alive',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br','Accept-Language':'en-US,en;q=0.5'
        }
        #print(header)
        return header

    # Function to return Proxy from list of working Proxies
    def return_proxy(self):
        return self.data['proxies'][random.randint(0,len(self.data['working_proxies'])-1)]
    
    # Scrap User Agents from List provided in JSON file
    def scrap_user_agents(self):
        for link in self.data['user_agents_links']:
            try:
                site=requests.get(link)
                if site.status_code == requests.codes.ok:
                    self.logger.info('Successfully got Link -> {}'.format(link))
                    html_soup = BeautifulSoup(site.text , 'html.parser')
                    response = html_soup.find_all('tr')
                    for res in response[1:]:
                        self.data['user_agents_scrap'].append(res.td.a.text)
                else:
                    self.logger.debug('Status Code Mismatch -> {}'.format(link))
                time.sleep(random.randint(0,10))
            except Exception as E:
                self.logger.warning('Error Occured -> {} with Exception {}'.format(link,E))

    # Get proxies from Pubproxy
    def get_pubproxy(self , limit = 20):
        self.logger.info('Gettting Proxy from Pubproxy .. ')
        proxies = []
        for i in range(limit):
            try:
                proxy = requests.get(self.pubproxy).json()['data'][0]['ipPort']
                if proxy not in proxies:
                    proxies.append(proxy)
            except Exception as E:
                self.logger.error('Something Went Wrong in Extracting from PubProxy .. ')
        self.logger.info('Called {} number of Proxies from PubProxy'.format(len(proxies)))
        return proxies

    # Get proxies from ProxyScrape
    def get_proxyscrape(self):
        try:
            response = requests.get(self.proxyscrape)
            if response.status_code == requests.codes.ok:
                proxies = response.text.split('\r\n')
                self.logger.info('Called {} number of Proxies from ProxyScrape'.format(len(proxies)))
                return proxies
            else:
                self.logger.error('Status Code Mismatch From ProxyScrape .. ')
                return '0'
        except Exception as E:
            self.logger.error('Something went Wrong in Extracting from ProxyScape .. -> {}'.format(E))
            return '0'

    # Get proxies from Free Proxy List
    def get_free_p_l(self):
            try:
                response = requests.get(self.free_p_l)
                if response.status_code==requests.codes.ok:
                    """page_soup = BeautifulSoup(response.text, "html.parser")
                    textarea = page_soup.find('textarea').text
                    proxies = re.findall('\d+\.\d+\.\d+\.\d+\:\d+',textarea)
                    self.logger.info('Called {} number of Proxies from free-proxy-list ..'.format(len(proxies)))
                    """
                    proxies = []
                    page_soup = BeautifulSoup(response.text, "html.parser")
                    table = page_soup.find_all("table")[0]
                    
                    rows = table.find_all("tr")
                    for row in rows:
                        proxy_row_data = row.find_all("td")
                        if len(proxy_row_data) > 0:
                            ip = proxy_row_data[0].text
                            port = proxy_row_data[1].text
                            full_proxy = ip+":"+port
                            proxies.append(full_proxy)
                    #for 
                    #print(textarea)
                    #proxies = re.findall('\d+\.\d+\.\d+\.\d+\:\d+',textarea)
                    self.logger.info('Called {} number of Proxies from free-proxy-list ..'.format(len(proxies)))
                    
                    return proxies
                else:
                    self.logger.error('Status Code Mismatch From free-proxy-list .. ')
                    return '0'
            except Exception as E:
                self.logger.error('Something went Wrong in Extracting from free-proxy-list .. -> {}'.format(E))
                print(E)
                return '0'

    # To filter Duplicated Proxies
    def get_proxies(self):
        self.data['proxies'] = self.get_free_p_l()
        self.data['proxies'] = list(filter(None , self.data['proxies']))

    # To save json data in disk
    def save_data(self):
        with open(self.data_file, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)

"""if __name__ == "__main__":
    pro = Proxies()
    pro.get_proxies()
    pro.save_data()
    try:
        send_proxies = pro.return_proxy()
        send_header = pro.return_header()
        url = 'https://www.azlyrics.com/lyrics/taylorswift/dropsofjupiter.html'
        response = requests.get(url , headers = send_header , proxies = {'http':send_proxies,'https':send_proxies} ,timeout = 10)
        if response.status_code == response.codes.ok:
            print('Everyhing Is Working...')
        else:
            print('Something Wrong...!!!..Unexpected Response Code')
    except Exception as E:
        print(E)
        print('Error Encountered')"""
        