#Imports
from bs4 import BeautifulSoup
import requests , re , random , os ,time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
import json
import logging
from datetime import datetime
from proxies import *

"""
#Proxy Checker

Takes proxy target name (az, lastfm, wiki, )

Takes in a URL the proxy is checking checking 

"""

def getFullFilePathForProxyHeaderDetails(target_name):
    return "header-json/" + target_name +"-header-details.json"

class Proxy_Checker(Proxies):
    def __init__(self, proxy_target_name, check_url):
        Proxies.__init__(self, getFullFilePathForProxyHeaderDetails(proxy_target_name))
        self.proxy_target_name = proxy_target_name
        self.check_url = check_url #'https://www.azlyrics.com/'
        
        if self.needToGetProxies():
            self.setup_proxies()
        
    def setup_proxies(self):
        self.get_proxies()
        self.scrap_user_agents()
        self.async_get_proxies()
        self.save_data()	

    def fetch(self, proxies):
        try:
            with requests.get(self.check_url , proxies = {'http':proxies,'https':proxies} ,timeout = 10) as response:
                if response.status_code == requests.codes.ok:
                    self.logger.info('SuccessFul Proxy-> {}'.format(proxies))
                    return proxies
                else:
                    self.logger.warning('Status Code {} Mismatch Proxy-> {}'.format(response.status_code,proxies))
                    return '0'
        except Exception as E:
            self.logger.warning('Timeout Proxy-> {}'.format(proxies))
            return '0'

    async def check_proxies(self):
        proxies = self.data['proxies']
        self.data['working_proxies'] = []

        with ThreadPoolExecutor(max_workers = 50) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                    loop.run_in_executor(executor , self.fetch , pro)
                    for pro in proxies
                    ]
            for response in await asyncio.gather(*tasks):
                if response != '0':
                    self.data['working_proxies'].append(response)
    
    def async_get_proxies(self):
        try:    
            self.loop = asyncio.get_event_loop()
            self.loop.set_debug(1)
            future = asyncio.ensure_future(self.check_proxies())
            self.loop.run_until_complete(future)
        except Exception as E:
            self.logger.warning(E)
        finally:
            self.loop.close()
			
			
"""if __name__ == "__main__":
    pro = Proxy_Checker("azlyrics", 'https://www.azlyrics.com/')
    pro.get_proxies()
    pro.async_get_proxies()
    pro.save_data()	
"""    