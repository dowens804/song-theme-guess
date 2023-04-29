#Imports
from bs4 import BeautifulSoup
import requests , re , random , os ,time,sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from unidecode import unidecode
from proxy_checker import *


'''

Wikipedia search for song data (duration, year)

https://en.wikipedia.org/wiki/So_Cold_(Breaking_Benjamin_song)


'''

def base_url():
    #https://en.wikipedia.org/w/index.php?curid=1979060
    #https://en.wikipedia.org/w/rest.php/v1/search/page?q=
    return 'https://en.wikipedia.org/w/'

def get_param_string(param):
    return param.replace(' ', '%20')

def get_url_string(artist_name, song_name):
    artist = get_param_string(artist_name)
    s_name = get_param_string(song_name)
    return 'https://en.wikipedia.org/w/rest.php/v1/search/page?q={}_{}'.format(artist, s_name)

def get_duration(min_str, sec_str):
    
    return (int(min_str) * 60) + int(sec_str)

class Wiki(Proxy_Checker):

    def __init__(self):
        Proxy_Checker.__init__(self, "wiki", base_url())
        self.base_url = base_url()
        self.url_max_retrires = 5
        self.max_retries = 5
        self.max_workers = 100
        self.timeout = 10
        # Read data : lyrics-genre-data.json
        # Updated- data: wiki-data.json
        # data-to scrap : wiki-data-to-scrap.json
        
        self.wiki_link_scrap_data = 'wiki_data_to_scrap.json'      #update
        self.wiki_link_duration_data = 'wiki_temp_data.json'        #
        self.read_data = 'lyrics-genre-data.json'       #
        
        self.wiki_load_data()
        self.az_logger()
        
        self.add_urls_from_read_data()

    def wiki_load_data(self):
        self.wiki_scrap_data = json.load(open(os.path.abspath(self.wiki_link_scrap_data) , 'r'))
        self.wiki_data = json.load(open(os.path.abspath(self.wiki_link_duration_data) , 'r'))
        self.song_data = json.load(open(os.path.abspath(self.read_data) , 'r'))

    def az_logger(self):
        self.az_logger = logging.getLogger(__name__)
        self.az_logger.setLevel(logging.DEBUG)
        self.az_formatter = logging.Formatter('%(asctime)s : %(filename)s : %(funcName)s : %(levelname)s : %(message)s')
        self.az_file_handler = logging.FileHandler(os.path.abspath('main.log'))
        self.az_file_handler.setLevel(logging.DEBUG)
        self.az_file_handler.setFormatter(self.az_formatter)
        self.az_logger.addHandler(self.az_file_handler)

    def save_wiki_scrap_data(self): #update data to scrap
        with open(self.wiki_link_scrap_data, 'w') as outfile:
            json.dump(self.wiki_scrap_data, outfile, indent=4)

    def save_wiki_data(self): #update data from wiki
        with open(self.wiki_link_duration_data , 'w') as outfile:
            json.dump(self.wiki_data , outfile, indent=4)
    
    def update_urls_in_scrap_data(self):
        for scrape_data in self.wiki_scrap_data["simple_urls"]:
            if scrape_data["wiki_page_url"] == "" and scrape_data["wiki_id"] > 0:
                wiki_id = scrape_data["wiki_id"]
                wiki_url = "https://en.wikipedia.org/w/index.php?curid=" + str(wiki_id)
                scrape_data["wiki_page_url"] = wiki_url
    
    def add_urls_from_read_data(self):
        if len(self.wiki_scrap_data["simple_urls"]) == 0:
            for song_data in self.song_data["data"]:
                artist = song_data["artist"]
                song_name = song_data["song_name"]
                
                full_url = get_url_string(artist, song_name)
                
                data_dic = {
                    "artist": artist,
                    "song_name": song_name,
                    "wiki_id": -1,
                    "wiki_url_for_id": full_url,
                    "wiki_page_url": ""
                }
                
                self.wiki_scrap_data["simple_urls"].append(data_dic)
                
            self.save_wiki_scrap_data()
            return
        """else:
            self.update_urls_in_scrap_data()
            self.save_wiki_scrap_data()
        
            1) get artsit and song name 
            
            2) perform search here to get wiki id :
            
            3) add wiki id to wikipedia url 
            
            4) add that url to simple urls 
        """
        
    def get_scrape_data_wiki(self , url, getHtml = True):
        flag = self.url_max_retrires
        while(flag):
            header = self.return_header()
            proxy = self.return_proxy()
            try:
                site = requests.get(url , headers = header , proxies = {'http':proxy,'https':proxy},timeout = self.timeout)
                if site.status_code == requests.codes.ok:
                    if getHtml:
                        html_soup = BeautifulSoup(site.text , 'html.parser')
                    
                        return html_soup
                    else :
                        return json.loads(site.json())
                    
                else:
                    self.az_logger.debug('Proxy Status Mismatch -> {} using Proxy -> {} on Try -> {}'.format(site.status_code , proxy , flag))
                    flag -= 1
                    if flag ==0:
                        return '0'
            except Exception as E:
                self.az_logger.debug('Something Went Wrong -> {} using  Proxy -> {} Error -> {} on try-> {}'.format(url,proxy,E,flag))
                flag -= 1
                if flag == 0:
                    return '0'
        return '0'
        
    def wiki_data_from_link(self , scrap_data):
        if scrape_data["wiki_page_url"] == "":
            link = scrap_data['wiki_url_for_id']
            data_json = self.get_scrape_data(link, false)
            
            try:
                wiki_id = data_json['pages'][0]['id']
                for data in self.wiki_scrap_data["simple_urls"]:
                    if data['wiki_url_for_id'] == scrap_data['wiki_url_for_id']:
                        data['wiki_id'] = wiki_id
                        data['wiki_page_url'] = "https://en.wikipedia.org/w/index.php?curid=" + str(wiki_id)
                        break 
                return {'link':link}        
            except Exception as E:
                self.az_logger.warning('Error in Scrapping genres {} Lineno.->{}'.format(E , sys.exc_info()[-1].tb_lineno))
                return '0'
            
        else:
            link = scrap_data['wiki_page_url']
            html_soup = self.get_scrape_data(link)
            
            if html_soup != '0':
        
                try:
                    published = html_soup.find('span', class_='published').string
                    pub_date_year = published.split('-')[0]
                    
                    try :
                        minutes = html_soup.find_all('span' , class_ = 'min')
                        
                        seconds = html_soup.find_all('span' , class_ = 's')
                        
                        finalDur = get_duration(minutes, seconds)
                    except :
                        finalDur = 0
                    
                    return {'link':link, 'artist':scrap_data['artist'] , 'song_name':scrap_data['song_name'] , 'duration': finalDur, "year": pub_date_year}
                except Exception as E:
                    self.az_logger.warning('Error in Scrapping genres {} Lineno.->{}'.format(E , sys.exc_info()[-1].tb_lineno))
                    return '0'
            else:
                return '0' 
    
    def get_all_urls_not_updated(self, dict_key):
        unsuccess = []
        for list_batch in self.wiki_scrap_data['simple_urls']:
            if list_batch[dict_key] not in self.wiki_data['completed']:
                unsuccess.append(list_batch)
                
        #print(len(unsuccess))
           
    async def get_batch_wiki(self, dict_key):
        unsuccess = []
        for list_batch in self.wiki_scrap_data['simple_urls']:
            if list_batch[dict_key] not in self.wiki_data['completed_'+ dict_key]:
                unsuccess.append(list_batch)
                
        self.az_logger.info('UnSuccessFul links {}'.format(unsuccess[0]))
        flag = self.max_retries
        while(flag):
            try:
                with ThreadPoolExecutor(max_workers = self.max_workers) as executor:
                    loop = asyncio.get_event_loop()
                    tasks = [
                            loop.run_in_executor(executor , self.wiki_data_from_link , pro)
                            for pro in unsuccess
                    ]
                    for response in await asyncio.gather(*tasks):
                        if response != '0':
                            #if dict_key == "wiki_url_for_id":
                                #for list_batch in self.wiki_scrap_data['simple_urls']:
                                    
                                
                            if dict_key == "wiki_page_url":
                                self.wiki_data['data'].append(response)
                                self.wiki_data['completed_'+ dict_key].append(response['link'])
                                
                            unsuccess.remove(response['link'])
                                
                    if len(unsuccess) == 0:
                        flag = 0
                    else:
                        flag -= 1
            except Exception as E:
                self.az_logger.warning('Scrapping Went Wrong -> {} Lineno. -> {}'.format(E , sys.exc_info()[-1].tb_lineno))
            finally:
                self.save_wiki_data()
        self.az_logger.info('Scrapped Successful... No. of genres in file is  {}'.format(len(self.wiki_data['completed'])))
        self.save_wiki_scrap_data()
        self.save_wiki_data()

    def start_scrapping(self, dict_key):
        try:
            #self.loop = asyncio.get_running_loop()
            #self.loop.set_debug(1)
            #loop.create_future()
            future = asyncio.ensure_future(self.get_batch_wiki(dict_key))
            #self.loop.create_future(self.get_batch_wiki(dict_key))
            t = asyncio.create_task(self.get_batch_wiki(dict_key))
            asyncio.run(t)
            future = asyncio.Future(t, self.loop)
            #test = asyncio.ensure_future(future)
            #self.loop.run_until_complete(test)
        except Exception as E:
            self.az_logger.warning('Warning Log -> {} Lineno -> {}'.format(E, sys.exc_info()[-1].tb_lineno))
        #finally:
            #self.loop.close()

if __name__ == "__main__":

    wiki = Wiki()
    #last_fm.get_all_urls_not_updated()
    
    #last_fm.wiki_data_by_list("New")
    #link = "https://www.last.fm/music/Beyonc%C3%A9/_/Naughty+Girl/+tags"
    #test = last_fm.genre_data_from_link(link)
    #print(test)
    #last_fm.start_scrapping()
    
    """
    "wiki_url_for_id":
    "wiki_page_url":
    """
    
    
    dict_key = "wiki_url_for_id"
    wiki.start_scrapping("wiki_url_for_id")
    
    
    dict_key = "wiki_page_url"
    
    
    
    '''user = input("Enter command or 'help' : ")
    while user != 'end':
        
        if user == 'help':
            print("'gcount : get the count of remaining genere calls'")
            print("'gdata' : start collecting data")
            print("'end' : end script")
            
        elif user == 'gcount':
            last_fm.get_all_urls_not_updated()
            
        elif user == 'gdata':
            last_fm.start_scrapping()
            
        else:
            print("invlaid command : "+ user)
            
        user = input("Enter command or 'help' : ")'''  
            