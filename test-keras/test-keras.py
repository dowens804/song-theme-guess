import pandas as pd
import tensorflow as tf

"""
Add to data 

relevant word count 
    how many words/phrases in our association list appear in the song

total weight from words

break up each word with its relevalncy?
    like each colum would be a word, 
    and the colum data would be, do this song contain that word
    the frequency of that word
    and the 
    
    
    Does higher associated word rate mean more likey chance of being a love song???
        we will keep weight out of this for now 
        only care about the word count
    
    colums 
    duration (sec)| year (int)| genre_num (int)| association word_1_count (int)| association word_2_count (int)| 
    
genre num
    assign all genres a num
    need to add genres

"""



test_train = pd.read_csv(
    r"C:\Users\dowen\Desktop\song-theme-guess\test-keras\train-data.csv",
    names=[
        "artist",
        "song_name",
        "duration",
        "year",
        "lyrics",
    ],
)

#print(test_train.head())

test_quess = pd.read_csv(
    r"C:\Users\dowen\Desktop\song-theme-guess\test-keras\guess-data.csv",
    names=[
        "artist",
        "song_name",
        "duration",
        "year",
        "lyrics",
    ],
)

#print(test_quess.head())


dataset = tf.data.Dataset.from_tensor_slices((test_train.values, test_train.pop('year').values))
 
for data, labels in dataset.take(1):
    print(data)
    print(labels)