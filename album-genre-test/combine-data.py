#Combine lyrice and genre data 
import json
import os

class CombineData():

    def __init__(self):
        self.lyricData_filename = 'data_lyrics.json'
        self.genreData_filename = 'data_genres.json'
        self.combinedData_filename = 'lyrics-genre-data.json'
        self.genres = {}
        self.load_data()
        
    def load_data(self):
        self.lyricData = json.load(open(os.path.abspath(self.lyricData_filename) , 'r'))["lyrics"]
        self.genreData = json.load(open(os.path.abspath(self.genreData_filename) , 'r'))["genres"]
        self.combinedData = json.load(open(os.path.abspath(self.combinedData_filename) , 'r'))
    
    def saveCombinedData(self, dataToSave):
        self.combinedData["genreList"] = self.genres
        
        self.combinedData["data"] = dataToSave
        
        self.combinedData["totalCount"] = len(dataToSave)
        
        with open(self.combinedData_filename, 'w') as outfile:
            json.dump(self.combinedData, outfile, indent=4)
            print("Saved Data!")
            
    def createDataPoint(self, genreData, lyricData):
        return {
            "link": lyricData["link"],
            "artist": genreData["artist"],
            "song_name": genreData["song_name"],
            "genre_list": genreData["genre_list"],#"genre_list"
            "lyrics" : lyricData["lyrics"]
        }
    
    def genreDataAndLyricDataMatch(self, genreData, lyricData):
        artistMatch = genreData["artist"].lower() in lyricData["artist"].lower()
        songMatch = genreData["song_name"].lower() == lyricData["song_name"].lower()
        return artistMatch and songMatch
    
    def updateGenres(self, newGenreList):
        for genre in newGenreList:
            if genre in self.genres.keys():
                self.genres[genre] = self.genres[genre] + 1
            else:
                self.genres[genre] = 1
                   
    def perform(self):
        cd_list = []
        #try:
        for lyric in self.lyricData:
            for genre in self.genreData:
                if self.genreDataAndLyricDataMatch(genre, lyric):
                    combinedData = self.createDataPoint(genre, lyric)
                    if combinedData not in cd_list:
                        cd_list.append(combinedData)
                        self.updateGenres(combinedData["genre_list"])
                        
        #except Exception as E:
        #    print(E)
            
        #finally:
        self.saveCombinedData(cd_list)
            
if __name__ == "__main__":
    
    #cd = CombineData()
    #cd.perform()
    
    