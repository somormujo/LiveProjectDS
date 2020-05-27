'''
Created on 12 may. 2020

@author: pascui
'''

import pandas as pd
import matplotlib as plt
import sys
import re
import time
from nltk.tokenize import WordPunctTokenizer

# Regular expressions to clean up data (table, html tags, links and equations 
reTable = re.compile(r"(?P<table>(<pre><code>.*?</code></pre>))")
reTag = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
reLinks = re.compile(r"^https?:\/\/.*[\r\n]*")
reTex = re.compile(r"(\${1,2}(.*?)(\${1,2}))|"
                   r"(\\\()(.*?)\\\)|"
                   r"(\\\[)(.*?)\\\]|"
                   r"(\\begin\{equation\}(.*?)\\end\{equation\})"
                   )

# Cleans and tokenizes the text of stack exchange 
def cleanData(data):

    #First lower all letters and removes extra spaces/tabs
    data = " ".join(data.split())
    data = data.lower() 

    #Removes data tables
    result = True
    while result:
        result = reTable.search(data)
        if result != None:
            data = reTable.sub('', data)
    
    #Removes html tags
    result = True
    while result:
        result = reTag.search(data)
        if result != None:
            data = reTag.sub('', data)
    
    #Removes links
    result = True
    while result:
        result = reLinks.search(data)
        if result != None:
            data = reLinks.sub('', data)
            
    #Removes equations
    result = True
    while result:
        result = reTex.search(data)
        if result != None:
            data = reTex.sub('', data)

    #Tokenizes the data ussing ntlk tokenizer
    data = " ".join(WordPunctTokenizer().tokenize(data))

    return(data)

class Loader(object):
    '''
    classdocs
    '''
    df = []

    #reads the dataset
    def __init__(self, aFile):
        '''
        Constructor
        '''
        self.df = pd.read_csv(aFile)
        
    #cleans the dataset
    def clean(self):
        self.df['tokenized'] = self.df['text'].apply(cleanData)
        
    #filters data by post id column, useful to create an small working set
    def filterPostId(self, a_post_id):
        return(self.df[self.df.post_id.eq(a_post_id)])
        
if __name__ == "__main__":
    """
    myDS = Loader("E:\Projects\git\LiveProjectDS\Dataset\stackexchange_812k.csv")
    
    print(myDS.df[8:15])
    
    smallerDS = myDS.filterPostId(279940)
    smallerDS.to_csv("E:\Projects\git\LiveProjectDS\Dataset\small.csv", index=False)
    
    print(smallerDS.head())
    """
    
    #store start time
    start_time = time.time()

    #Loads small working set, cleans the data and save it to another file
    myDS = Loader("E:\Projects\git\LiveProjectDS\Dataset\small.csv")
    myDS.clean()
    myDS.df.to_csv("E:\Projects\git\LiveProjectDS\Dataset\clean.csv", index=False)

    #Loads the complete working set, cleans the data and save it to another file
    myDS = Loader("E:\Projects\git\LiveProjectDS\Dataset\stackexchange_812k.csv")
    myDS.clean()
    myDS.df.to_csv("E:\Projects\git\LiveProjectDS\Dataset\stackexchange_812k-clean.csv", index=False)
    
    #prints total time taken
    print("--- %s seconds ---" % (time.time() - start_time))    

    #
    