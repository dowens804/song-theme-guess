
import requests , re , random , os ,time
import musicbrainzngs
import json
import asyncio
import time
"""
https://python-musicbrainzngs.readthedocs.io/en/v0.7.1/api/#searching

great ref for asyncio : https://www.twilio.com/blog/working-with-files-asynchronously-in-python-using-aiofiles-and-asyncio

"""
def printDict(data_dict):
    for key in data_dict.keys():
        data = data_dict[key]
        print(f"{key} : {str(data)}")
        
def getYear(date_string):
    date_split = date_string.split('-')
    return date_split[0]
        
class MusicBrainzClient: # used to get year and duration
    def __init__(self):
        self.data_file = 'base-data.json'
        self.updated_data_file = 'updated-data.json'
        musicbrainzngs.set_useragent(
            "Song Analysis",
            "0.1",
            "https://github.com/dowens804/song-theme-guess",
        )
        self.loadData()

    def loadData(self):
        self.data = json.load(open(os.path.abspath(self.data_file) , 'r+'))["data"]
        self.updated_data = json.load(open(os.path.abspath(self.updated_data_file) , 'r+'))["data"]
    
    def saveData(self):
        with open(self.updated_data_file, '+w') as outfile:
            final = {'data': self.data}
            json.dump(final, outfile, indent=4)
            
            
    async def searchRecording(self, songBlock, index):
        print(f"started search for {songBlock['song_name']}")
        artist = songBlock['artist']
        songName = songBlock['song_name']
        try:
            clientData = musicbrainzngs.search_recordings(query=songName, artistname=artist, limit=5)
            newData = clientData['recording-list'][0]
            
            return {
                'index': index, 
                'duration': newData["length"],
                'year': getYear(newData["release-list"][0]['date']),
                'artist': artist,
                'song_name': songName
            }
        except Exception as e:
            print(e)
            return {}
            
    def searchRelease(self, songBlock):
        artist = songBlock['artist']
        songName = songBlock['song_name']
        test = musicbrainzngs.search_releases(query=songName, artistname=artist, limit=5)
        return test['release-list']
          
    async def getNewSongData(self):
        tasks = []
        for index in range(len(self.data)):
        
            currentData = self.updated_data[index]
            
            if "duration" not in currentData.keys():
                tasks.append(asyncio.ensure_future(self.searchRecording(currentData, index)))
            else:
                self.data[index]['duration'] = currentData["duration"]
                self.data[index]['year'] = currentData["year"]
                
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
                    self.data[index]['duration'] = newData["duration"]
                    self.data[index]['year'] = newData["year"]
                               
        try :
            self.normalizeData()
            
        except Exception as e: 
            print("failed to normalize")
            print(e)
    
    def testSearch(self):
        test1 = self.searchRecording(self.data[0])
        
        test2 = self.searchRelease(self.data[5])
        
        print("recording :")
        print("------------------------------------------------")
        printDict(test1[0])
            
        print("release : ")
        print("------------------------------------------------")
        printDict(test2[0])
        
        
    def normalizeData(self):
        for index in range(len(self.data)):
            currentData = self.data[index]
            if "duration" not in currentData.keys():
                self.data[index]['duration'] = -1
                
            if "year" not in currentData.keys():
                self.data[index]["year"] = -1
                
              
if __name__ == '__main__':
    
    test = MusicBrainzClient()
    #test.testSearch()
    
    #newData = await test.getNewSongData()
    tic = time.perf_counter()
    
    #test.normalizeData()
    asyncio.run(test.getNewSongData())
    
    toc = time.perf_counter()
    print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")
    
    
    
    