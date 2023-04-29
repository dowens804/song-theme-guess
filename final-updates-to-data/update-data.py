import json
import requests , re , random , os ,time

class UpdateData:

    def __init__(self):
        self.data_file = 'base-data.json'
        self.updated_data_file = 'updated-data.json'
        
        self.loadData()
    
    def loadData(self):
        self.data = json.load(open(os.path.abspath(self.data_file) , 'r+'))["data"]
        #self.updated_data = json.load(open(os.path.abspath(self.updated_data_file) , 'r+'))["data"]
    
    def saveData(self):
        with open(self.updated_data_file, '+w') as outfile:
            final = {'data': self.data}
            json.dump(final, outfile, indent=4)
                 
    def getWordCount(self, lyrics):
        initLyrics = lyrics
        #first pass : remove '\t' and ')' and '(' with nothing
        first_pass = initLyrics.replace('\t', '').replace(')', '').replace('(', '')
        
        #second pass: split first pass by '\n' 
        noNewLineList = first_pass.split('\n')
        
        totalCount = 0
        finalWordsList = []
        for piece in noNewLineList:
            if len(piece) > 0 and piece != "":
                filterdPiece = piece.replace(',', '').replace('?', '').replace('!', '').replace('"', '').replace("'", '')
                words = list(map(lambda x : x.lower(), filterdPiece.split(' ')))
                finalWordsList.extend(words)
                totalCount = totalCount + len(words)
            
        return len(finalWordsList)
        
    def updateDataWithWordCount(self):
        for index in range(len(self.data)):
            data = self.data[index]
            
            lyrics = data["lyrics"]
            wordCount = -1
            try:
                wordCount = self.getWordCount(lyrics)
            except Exception as e:
                print(f'couldnt get word count for : {data["song_name"]}')
                print(e)
                
            self.data[index]["word_count"] = wordCount
        
        self.saveData()

    def testGetWordCount(self):
        return self.getWordCount(self.data[100]["lyrics"])
    
if __name__ == '__main__':
    
    test = UpdateData()
    test.updateDataWithWordCount()
    
    