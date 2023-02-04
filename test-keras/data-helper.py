#script to help with formating data 

"""
pre script steps:

create genere num dictioanry , add to file
create associated word list, add to file 
add genres to test and learn files


"""


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
		
	
7 export that file

"""