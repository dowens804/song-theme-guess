# make my own rotating proxy
#Imports
from bs4 import BeautifulSoup
import requests , re , random , os ,time
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime
from pathlib import Path

TIMEOUT_IN_SECONDS = 10

class CollectRotatingProxyData:
    
    def __init__(self, checkUrl):
        self.proxyscrape = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=elite'
        self.free_p_l = 'https://free-proxy-list.net/'
        self.data_file = 'proxy_data.json'
        
        self.read_proxy_json()
        self.checkUrl = checkUrl
        self.update()
        
    
    def update(self):
        if self.userAgents == []:
            self.get_new_user_agents()
        
        if self.ipAddr == []:
            self.get_new_ip_addrs()
        
        if self.workingIpAddr == []:
            asyncio.run(self.get_working_ip_addrs())
            
        self.update_proxy_json()
        self.save_proxy_json()
        print("done!")
        
    def save_proxy_json(self):
        with open(self.data_file, 'w') as outfile:
            json.dump(self.data, outfile, indent=2)

    def read_proxy_json(self):
        data = json.load(open(os.path.abspath(self.data_file) , 'r+'))
        
        self.userAgents = data["user_agent_data"]["user_agents_scrap"]
        self.userAgentLinks = data["user_agent_data"]["user_agents_links"]
        self.ipAddr = data["ip_addr"] 
        self.workingIpAddr = data["working_ip_addr"]
        self.referrer = data["referrer"]
        self.last_updated = data["last_updated"]
        
        self.data = data
        
    def update_proxy_json(self):
        self.data["user_agent_data"]["user_agents_scrap"] = self.userAgents
        self.data["user_agent_data"]["user_agents_links"] = self.userAgentLinks
        self.data["ip_addr"] = self.ipAddr
        self.data["working_ip_addr"] = self.workingIpAddr
        self.data["last_updated"] = str(datetime.now())
        
        self.save_proxy_json()
        
    def get_new_ip_addrs(self):
        try:
            response = requests.get(self.free_p_l)
            if response.status_code==requests.codes.ok:
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
                
                print('Called {} number of Proxies from free-proxy-list ..'.format(len(proxies)))
                
                self.ipAddr = proxies
            else:
                print('Status Code Mismatch From free-proxy-list .. ')
                #return '0'
        except Exception as E:
            print('Something went Wrong in Extracting from free-proxy-list .. -> {}'.format(E))
            print(E)
            #return '0'
        """try:
            response = requests.get(self.proxyscrape)
            if response.status_code == requests.codes.ok:
                ip_addresses = response.text.split('\r\n')
                self.ipAddr = ip_addresses
                print('Called {} number of Proxies from ProxyScrape'.format(len(proxies)))
                #return proxies
            else:
                print('Status Code Mismatch From ProxyScrape .. ')
                #return '0'
        except Exception as E:
            print('Something went Wrong in Extracting from ProxyScape .. -> {}'.format(E))"""
            
    
    async def check_proxy(self, url, ipaddr):
        proxy = 'https://' + ipaddr
        try:
            session_timeout = aiohttp.ClientTimeout(total=None,
                                                    sock_connect=TIMEOUT_IN_SECONDS,
                                                    sock_read=TIMEOUT_IN_SECONDS)
            async with aiohttp.ClientSession(timeout=session_timeout) as session:
                async with session.get(url, proxy=proxy, timeout=TIMEOUT_IN_SECONDS) as resp:
                    return proxy
        except Exception as error:
            # you can comment out this line to only see valid proxies printed out in the command line
            print('Proxy responded with an error: ', error)
            return '0'
    
    async def get_working_ip_addrs(self):
        tasks = []
        
        for ipaddr in self.ipAddr:
            #proxy = 'http://' + ipaddr
            task = asyncio.create_task(self.check_proxy(self.checkUrl, ipaddr))
            tasks.append(task)

        #await asyncio.gather(*tasks)
        for response in await asyncio.gather(*tasks):
            if response != '0':
                self.workingIpAddr.append(response)
    
    def get_new_user_agents(self):
        for link in self.userAgentLinks:
            try:
                site=requests.get(link)
                if site.status_code == requests.codes.ok:
                    self.logger.info('Successfully got Link -> {}'.format(link))
                    html_soup = BeautifulSoup(site.text , 'html.parser')
                    response = html_soup.find_all('tr')
                    for res in response[1:]:
                        self.userAgents.append(res.td.a.text)
                else:
                    print('Status Code Mismatch -> {}'.format(link))
                time.sleep(random.randint(0,10))
            except Exception as E:
                print('Error Occured -> {} with Exception {}'.format(link,E))
                
    def return_header(self):
        header = {
                'user-agent':self.userAgents[random.randint(0,len(self.userAgents)-1)] , 
                'referer':self.referrer[random.randint(0,len(self.referrer)-1)],
                'Upgrade-Insecure-Requests': '0' , 
                'DNT':'1' , 
                'Connection':'keep-alive',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br','Accept-Language':'en-US,en;q=0.5'
        }
        return header
    
if __name__ == "__main__":
    pro = CollectRotatingProxyData('https://www.azlyrics.com/')
    
        
    
"""class RotatingProxy():

    def __init___(self, checkUrl):
        self.data = data
        self.checkUrl = 
        self.collectData = CollectRotatingProxyData(checkUrl)
        
        
        """
        

    
