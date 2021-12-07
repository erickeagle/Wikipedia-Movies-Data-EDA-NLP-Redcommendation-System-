#loading the libaries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
# we are using counter for counting the number of times a particaular word occurs
from collections import Counter
import sys
import logging

def main(df,word_length): 
    '''This is the main function of the program
    '''
    print('IN MAIN')
    #list of the unique genres
    choices_final=df['Genre_updated'].unique()[1:]
    # for making the list of most common words like 30, 50, 100 for a particular genre
    dax={choices:Counter(" ".join(df[df['Genre_updated']==choices]['Plot_cleanned']).split()).most_common(200) for choices in choices_final}
    data=pd.DataFrame(columns = ['Genre', 'Words', 'Counts'])
    for i in dax.keys():
        df1=pd.concat([pd.DataFrame([i for j in range(len(dax[i]))],columns=['Genre']),pd.DataFrame(dax[i],columns=['Words', 'Counts'])],axis=1)
        data=pd.concat([data,df1])
    data.to_csv(f"most_frequent_words_{word_length}_script.csv",index=False)

if __name__ == '__main__':
    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename = 'logs_count.log',
                        level = logging.DEBUG,
                        format = LOG_FORMAT,
                        filemode = 'w')  
    path=sys.argv
    logging.info('Started fetching')
    main(pd.read_csv(path[1]),path[2])
    logging.info('Fetching Done')