#script to help with formating data 
import pandas as pd
import json
"""
pre script steps:

create genere num dictioanry , add to file
create associated word list, add to file 
add genres to test and learn files


"""

genre_list = ["Alternative", "Blues", "Children’s Music", "Classical", "Comedy", "Country", "Dance / EMD", "Disney", "Electronic", "Hip-Hop/Rap", "Pop", "Holiday", "Jazz", "Opera", "R&B/Soul", "Reggae", "Rock", "Soundtrack", "Singer/Songwriter", "World"]
genre_dict = {'alternative': 1, 'blues': 2, 'children’s music': 3, 'classical': 4, 'comedy': 5, 'country': 6, 'dance / emd': 7, 'disney': 8, 'electronic': 9, 'hip-hop/rap': 10, 'rap': 10, 'pop': 11, 'holiday': 12, 'jazz': 13, 'opera': 14, 'r&b/soul': 15, 'reggae': 16, 'rock': 17, 'soundtrack': 18, 'singer/songwriter': 19, 'world': 20, 'electropop': 9}

aw_list = ['dearly', 'madly', 'passionately', 'tenderly', 'loving', 'cherish', 'affection', 'tenderness', 'adore', 'loving', 'fondly', 'passionate', 'hate', 'cherished', 'everlasting', 'beloved', 'dearest', 'him', 'caress', 'commandment', 'yearn', 'gentleness', 'longing', 'passion', 'beget', 'jealousy', 'aphrodite', 'happiness', 'beloved', 'devotion', 'neighbor', 'jealous', 'companionship', 'woo', 'lover', 'affectionate', 'dion', 'forever', 'darling', 'fondness', 'sorrow', 'tender', 'truly', 'selfish', 'sweetness', 'wed', 'ardent', 'confess', 'sake', 'earthly', 'neighbour', 'unworthy', 'nymph', 'marri', 'hopelessly', 'grief', 'kindness', 'deeply', 'sweet', 'loneliness', 'hatred', 'joy', 'suitor', 'despise', 'saviour', 'anguish', 'virtuous', 'vanity', 'forsake', 'heart', 'bosom', 'damsel', 'dear', 'aught', 'manly', 'hearted', 'beatles', 'sadness', 'delight', 'beseech', 'intimacy', 'fain', 'solitude', 'beauty', 'boyish', 'crave', 'kiss', 'sincere', 'pity', 'chivalry', 'charm', 'pang', 'esteem', 'soul', 'entreat', 'sincerity', 'be', 'soul', 'goodness', 'generosity',
'married', 'couple', 'relationship', 'bigamist', 'wife', 'marriage', 'heterosexual', 'marry', 'affair', 'wed', 'paramour', 'marital', 'newlywed', 'husband', 'girlfriend', 'sex', 'morganatic', 'fiancee', 'connubial', 'conjoin', 'honeymoon', 'ex', 'family', 'bachelor', 'fond', 'partner', 'conjugal', 'bridal', 'polygamy', 'kiss',
'love life', 'lovemaking', 'making love', 'sexual love', 'passion', 'beloved', 'dear', 'dearest', 'honey', 'enjoy', 'bang', 'be intimate', 'bed', 'bonk', 'do it', 'eff', 'fuck', 'get it on', 'get laid', 'have a go at it', 'have intercourse', 'have it away', 'have it off', 'have sex', 'hump', 'jazz', 'know', 'lie with', 'make love', 'make out', 'roll in the hay', 'screw', 'sleep together', 'sleep with', 'erotic love']

def getAwData_WordAssoApi():
    ret_list = []
    with open(r"C:\Users\dowen\Desktop\song-theme-guess\test-keras\love-stimulus.json") as file_object:
        aw_dict = json.load(file_object)
        items = aw_dict["response"][0]["items"]
        for data in items:
            ret_list.append(data["item"].lower())
    return ret_list


def getAwData_rapidApi():
    with open(r"C:\Users\dowen\Desktop\song-theme-guess\test-keras\rapid-api-love.json") as file_object:
        aw_dict = json.load(file_object)
        return aw_dict["associations_array"]


def getAwData_WordApi():
    ret_list = []
    with open(r"C:\Users\dowen\Desktop\song-theme-guess\test-keras\word-api-love.json") as file_object:
        aw_dict = json.load(file_object)
        return aw_dict["synonyms"]
 

def getTrainData():
    test_train = pd.read_csv(
        r"C:\Users\dowen\Desktop\song-theme-guess\test-keras\train-data.csv",
        names=[
            "artist",
            "song_name",
            "duration",
            "year",
            "genre",
            "isLoveSong",
            "lyrics",
        ],
    )
    
    return test_train


def getTestData():
    test_quess = pd.read_csv(
        r"C:\Users\dowen\Desktop\song-theme-guess\test-keras\guess-data.csv",
        names=[
            "artist",
            "song_name",
            "duration",
            "year",
            "genre",
            "isLoveSong",
            "lyrics",
        ],
    )
    
    return test_quess


def writeToCsv(data, filename):
    header = ['Name', 'M1 Score', 'M2 Score']
    #data = [['Alex', 62, 80], ['Brad', 45, 56], ['Joey', 85, 98]]
    #data must be in that format 
    data = pd.DataFrame(data)
    #r"C:\Users\dowen\Desktop\song-theme-guess\test-keras\love-stimulus.json"
    data.to_csv(r'C:\Users\dowen\Desktop\song-theme-guess\test-keras\updated-' + filename + '.csv', index=False)
    
    return
    
    
def getWordCountOfLyrics(lyrics):
    return len(lyrics.split())
    
    
def getCountOfWordsInDictionary(lyrics, aw_list):
    lyric_word_list = lyrics.split()
    count_dict = {}
    
    for word in lyric_word_list:
        if word in aw_list:
            if word in count_dict.keys():
                count_dict[word] = count_dict[word] + 1
            else:
                count_dict[word] = 1
    return count_dict          
    

#def formatDataForCsv

"""

Looks like my associated word list is not good 

now i need to try and get a training set from actual love songs 
    try to see if there is a corelation 


"""


def createBetterTrainData():
    data_list = []
    test_data = getTrainData();
    df = test_data.reset_index()  # make sure indexes pair with number of rows

    for index, row in df.iterrows():
        #print(row['artist'], row['song_name'])
        duration = row['duration']
        year = row['year']
        genre = row['genre'].lower()
        isLoveSong = row['isLoveSong']
        lyrics = row['lyrics'].lower()
        
        genreNum = genre_dict[genre]
        
        wordCount = getWordCountOfLyrics(lyrics)
        
        returnList = [duration, year, genreNum]
        
        aw_count_for_lyrics = getCountOfWordsInDictionary(lyrics, aw_list)
        aw_lyric_count_empty = len(aw_count_for_lyrics) != 0
        
        for word in aw_list:
            if(aw_lyric_count_empty or word not in aw_count_for_lyrics.keys()):
                returnList.append(0)
            else:
                returnList.append(aw_count_for_lyrics[word])
                
        returnList.append(isLoveSong)
        
        data_list.append(returnList)
        
    
    writeToCsv(data_list, "love-data-train")
    return data_list
            
        
        
        
        
    
def createGenreDict():
    ret_dict = {}
    count = 1
    for g in genre_list:
        ret_dict[g.lower()] = count
        count = count + 1
        
    return ret_dict
        
#updatedTestData = createBetterTrainData()
print(createBetterTrainData())

""""
1 open csv file 

2 read all data into a dictionary

3 get the lyric string 

4 do all the counting that needs to be done, based on assciated word list
	split lyric into space delimited list
	for each word in the string:
		if in association list: 
			add to 
		 
	
	for each association word that isnt in this new dictionary
		add the word, with count = 0
		
	do this for each song 
	
		the data will be very long 
	
5 create a new csv file 

6 read all relevant data into that file 
	for each song 
		add the duration
		add the year
		add genre num
		add the total word count
        
        add if it is a love song (0 = false, 1 = true)
		
	
7 export that file

"""