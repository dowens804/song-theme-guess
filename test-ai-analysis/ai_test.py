#
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
"""
I have collected all of my training data 

https://data-flair.training/blogs/train-test-set-in-python-ml/
"""



"""
https://www.digitalocean.com/community/tutorials/how-to-build-a-machine-learning-classifier-in-python-with-scikit-learn


Data Stucture

data = readDAtaFromFile

label_names = data['target_names'] -> this returns a list 

labels = data['target'] -> this returns a list 

feature_names = data['feature_names'] - this is list of labels associated with the label

features = data['data'] - lists of data values 



label_names = # in this example they are the classification labels ['rock_song', 'not_rock_song']

labels[0] =  #the clasification - either 0 or 1

feature_names[0] =  one of the features used for analysis

features[0] = data associated with the feature in the feature_names list 


create artist to number dict 

data = {
    "target_names": ['rock_song', 'not_rock_song'],
    "target": [0, 0 , 0, 1, 0, 1, 1, . . . ],
    "feature_names": ['year', 'word_count', 'duration', 'is_explicit', "artist" ],
    "data": [
        [], #year data 
        [], #word_count data
        [], #duration data
        [], #is_explicit
        []  #artist_data
    ],
    "artist_to_num": {} # save for later use
}

"""
import json
import requests , re , random , os ,time,sys
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.datasets import load_breast_cancer

def getTargetData(dataItem, genre_name):
    if genre_name in dataItem["genre_list"]:
        return 1
    else:
       return 0 
    
class FormatData():
    def __init__(self, genre_type):
        self.ai_data_file = f'ai-format-data-{genre_type}.json'
        self.genreType = genre_type
        self.data_file = 'data.json'
        self.loadData()
        
    def loadData(self):
        songData = json.load(open(os.path.abspath(self.data_file) , 'r'))
        self.data = songData['data']
        self.artistDict = songData["artist_to_num"]
        self.ai_data = {
            "target_names": [f'not_{self.genreType}_song', f'{self.genreType}_song' ],
            "target": [], # zero is not rock song , 1 is rock song
            "feature_names": ['year', 'word_count', 'duration', 'is_explicit', "artist" ],
            "data": [
            ],
            "artist_to_num": songData["artist_to_num"]
        }
    

    def getArtistDict(self):
        """artistDict = {}
        for item in self.data:
            #item = self.data[key]
            artist_name = item['artist']
            if len(artistDict.keys()) == 0:
                artistDict[artist_name] = 1
            elif artist_name not in artistDict.keys():
                artistDict[artist_name] = len(artistDict.keys())
        
        return artistDict"""
        return self.artistDict
     

    def saveData(self):
        with open(self.ai_data_file , 'w+') as outfile:
            json.dump(self.ai_data , outfile, indent=4)
            
    def formatData(self):
        artist_to_num = self.getArtistDict()
        
        #self.ai_data["artist_to_num"] = artist_to_num
        
        year_data = []
        target_data = []
        word_count = []
        duration = []
        is_explicit = []
        artist_data = []
        
        for data_item in self.data:
            
            
            """year = data_item["year"]
            if year == "":
                year_data.append(-1)  
            else :
                year_data.append(int(year))
                
            target_data.append(getTargetData(data_item, "rock"))
            word_count.append(data_item["word_count"])
            duration.append(int(data_item["duration"]))
            is_explicit.append(int(data_item["is_explicit"]))
            
            artist_data.append(artist_to_num[data_item['artist']])"""
            
            year_data = 0
            year = data_item["year"]
            if year == "":
                year_data = -1
            else :
                year_data = int(year)
                
            target_data.append(getTargetData(data_item, self.genreType))
            word_count = data_item["word_count"]
            duration = int(data_item["duration"])
            is_explicit = int(data_item["is_explicit"])
            
            artist_data = artist_to_num[data_item['artist']]
            
            
            
            temp_list = [year_data, word_count, duration, is_explicit, artist_data]
            self.ai_data["data"].append(temp_list)
        
        self.ai_data["target"] = target_data
        
        """self.ai_data["data"] = [
           year_data, word_count, duration, is_explicit, artist_data
        ]"""
        
        self.saveData()
        

class AiAnalysis():
    def __init__(self, genre_name):
        self.ai_data_file = f'ai-format-data-{genre_name}.json'
        self.genre_name = genre_name
        self.test_ai()
        
    def test_ai(self):
        
        # Load dataset
        data = json.load(open(os.path.abspath(self.ai_data_file) , 'r'))

        # Organize our data
        #label_names = data['target_names']
        labels = data['target']
        #feature_names = data['feature_names']
        features = data['data']

        # Look at our data
        #print(label_names)
        #print('Class label = ', labels[0])
        #print(feature_names)
        #print(features[0])

        # Split our data
        
        updatedFeatures = np.array(features)
        #print(updatedFeatures.shape)
        updatedLabels = np.array(labels)
        #print(updatedLabels.shape)
        
        train, test, train_labels, test_labels = train_test_split(updatedFeatures,
                                                                  updatedLabels,
                                                                  test_size=0.1,
                                                                  random_state=5)

        # Initialize our classifier
        gnb = GaussianNB()

        # Train our classifier
        model = gnb.fit(train, train_labels)

        # Make predictions
        preds = gnb.predict(test)
        #print(preds)

        # Evaluate accuracy
        print(self.genre_name)
        print(accuracy_score(test_labels, preds))
        print("///////////////////////////////////")
    
        
if __name__ == "__main__":

    genre_list = ["rnb", "pop", "hip-hop", "jazz", "rap", "alternative", "swing", "soul", "funk", "dance", "indie"]
    for g in genre_list:
        #test = FormatData(g)
        #test.formatData()
        test = AiAnalysis(g)

    #test = FormatData()
    #test = AiAnalysis()
    
    #test.formatData()
    
    #data = load_breast_cancer()
    
    
    