#importing the libraries
import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")
import nltk
from thefuzz import fuzz
from thefuzz import process
import sys
import logging
import string

def remove_punctuation(text):
    return ''.join([words.lower() for words in text if words not in string.punctuation])


def tokenization(text):
    return nltk.tokenize.word_tokenize(text)


stopwords = nltk.corpus.stopwords.words('english')
def stopwards(words):
    return [i for i in words if i not in stopwords]

lemma= nltk.WordNetLemmatizer()

def lemmatization(words):
    return ' '.join([lemma.lemmatize(word) for word in words])


def replace_year(x):
    l=re.findall("\d{4}", x)
    for i in l:
        x=x.replace(i, 'wxyz')
    return x








def main(df): 
    '''This is the main function of the program
    '''
    print('IN MAIN')
    replace_dict={"\r": " ","\n":" ",    }

    for key,items in replace_dict.items():
        df['Plot']= df['Plot'].str.replace(key,items)
        
    #replacing the year with wxyz   
    df['Plot_1'] = df['Plot'].apply(lambda x: replace_year(x))
    #removing punctuations and numbers
    df['plot_without_punct']=df['Plot_1'].apply(lambda x: re.sub(r'[0-9]', '',x)).apply(lambda x: remove_punctuation(x))
    #tokenization
    df['plot_tokenized']=df['plot_without_punct'].apply(lambda x: tokenization(x))
    #removing stopwards
    df['plot_tokenized_removed_sw']=df['plot_tokenized'].apply(lambda x: stopwards(x))
    #applying lemmatization
    df['plot_lemma']=df['plot_tokenized_removed_sw'].apply(lambda x: lemmatization(x))
    #making final dataframe
    df=df[['Release Year', 'Title', 'Origin/Ethnicity', 'Director', 'Cast', 'Genre','Genre_updated', 'Wiki Page', 'Plot', 'plot_lemma']]
    df.rename(columns={'plot_lemma': 'Plot_cleanned'},inplace=True)
    df.to_csv('wiki_movie_plots_deduped_cleaned_genre_and_plot_script.csv',index=False)





if __name__ == '__main__':
    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename = 'logs_plot.log',
                        level = logging.DEBUG,
                        format = LOG_FORMAT,
                        filemode = 'w')  
    path=sys.argv
    logging.info('Started fetching')
    main(pd.read_csv(path[1]))
    logging.info('Fetching Done')
