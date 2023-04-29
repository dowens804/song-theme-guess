import requests , re , random , os ,time
from ytmusicapi import YTMusic
import json
import asyncio
import time
"""
duration count  = 1050
total count = 1196


values we want 
    duration_seconds
    isE

is_explicit count = 1066

https://ytmusicapi.readthedocs.io/en/stable/index.html

"""
def printDict(data_dict):
    for key in data_dict.keys():
        data = data_dict[key]
        print(f"{key} : {str(data)}")

class YouTubeClient:

    def __init__(self): #used to get wether or not the song is explicit
        
        self.ytmusic = YTMusic()#YTMusic("browser.json")
        
        self.data_file = 'updated-data.json'
        self.updated_data_file = 'final-data-update.json'
        
        self.loadData()
              
    def loadData(self):
        self.data = json.load(open(os.path.abspath(self.data_file) , 'r+'))["data"]
        self.updated_data = json.load(open(os.path.abspath(self.updated_data_file) , 'r+'))["data"]
    
    def saveData(self):
        with open(self.updated_data_file, '+w') as outfile:
            final = {'data': self.data}
            json.dump(final, outfile, indent=4)
    
    async def searchForSong(self, songBlock, index):
        print(f"started search for {songBlock['song_name']}")
        try:
            artist = songBlock['artist']
            songName = songBlock['song_name']
            dataList = self.ytmusic.search(query= f"{songName} by {artist}", filter= 'songs', limit= 5, ignore_spelling= True)# → List[Dict]
            clientData = dataList[0]
            
            returnDict = {
                'index': index, 
                'is_explicit': clientData["isExplicit"],
                'artist': artist,
                'song_name': songName
            }
            
            if songBlock["duration"] == -1:
                returnDict["duration"] = clientData["duration_seconds"] * 100
            
            if songBlock["year"] == -1 :
                try:
                    albumId = clientData["album"]["id"]
                    returnDict["year"] = await self.searchForAlbumYear(albumId)
                except:
                    print("couldnt update song year")
                    
            return returnDict

        except Exception as e:
            print("is it here")
            print(e)
            return {}
             
    async def searchForAlbumYear(self, albumId):
        return self.ytmusic.get_album(albumId)["year"]
           
    async def getNewExplicitData(self):
        tasks = []
        for index in range(len(self.data)):
        
            currentData = self.updated_data[index]
            
            if "is_explicit" not in currentData.keys():
                tasks.append(asyncio.ensure_future(self.searchForSong(currentData, index)))
            else:
                self.data[index]['is_explicit'] = currentData["is_explicit"]
                     
        if len(tasks) > 0:        
            all_new_data = await asyncio.gather(*tasks)
            
            self.updateData(all_new_data)
            
            print("creating new data file")
            self.saveData()
            
        else: 
            print("All data updated")
        
    def updateData(self, newDataList):
        for newData in newDataList:
            if len(newData.keys()) > 0:
                index = newData['index']
                artist = newData['artist']
                savedData = self.data[index]
                
                if artist == savedData['artist']:
                    self.data[index]['is_explicit'] = newData["is_explicit"]
                
                if 'duration' in newData.keys():
                    self.data[index]['duration'] = newData["duration"]
                    
                if 'year' in newData.keys():
                    self.data[index]['year'] = newData["year"]

    def testSearch(self):
        test1 = self.searchForSong(self.data[0], 0)
        
        #test2 = self.searchRelease(self.data[5])
        
        print("data :")
        print("------------------------------------------------")
        printDict(test1[0])
            
if __name__ == '__main__':
    
    test = YouTubeClient()
    #test.testSearch()
    
    tic = time.perf_counter()
    asyncio.run(test.getNewExplicitData())
    #
    toc = time.perf_counter()
    print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")
    