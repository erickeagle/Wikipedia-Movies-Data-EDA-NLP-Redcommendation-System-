#importing the libraries

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import logging


#importing the data of the cleanned genre and plot
global df
df=pd.read_csv('wiki_movie_plots_deduped_cleaned_genre_and_plot.csv')
#importing the data of most frequent words/common words in the plot column for each genre
global data
data=pd.read_csv("most_frequent_words_30.csv")

#making a dict of the words
global dict_words
dict_words={i:(data[data['Genre']==i]['Words']).to_list() for i in data['Genre'].unique()}

#for making recommendations
def get_recommendations(title, cosine_sim, indices):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:10]
    movie_indices = [i[0] for i in sim_scores]
    return set(Train['Title'].iloc[movie_indices])

#function for reducing the words
def reduce_words(x):
    return ' '.join([i for i in x['Plot_cleanned'].split() if i in  dict_words[x['Genre_updated']]])
     


def main(movie_title): 
    '''This is the main function of the program
    '''
    print('IN MAIN')
    Train=df[~pd.isnull(df['Genre_updated'])]
    Train['Plot_trimmed']=Train[['Genre_updated','Plot_cleanned']].apply(lambda x: reduce_words(x),axis=1)
    tfidf_vectorizer = TfidfVectorizer(use_idf=True,ngram_range=(1,1))
    X_train_vectors_tfidf = tfidf_vectorizer.fit_transform(Train['Plot_trimmed']) 
    cosine_sim= cosine_similarity(X_train_vectors_tfidf , X_train_vectors_tfidf )
    indices = pd.Series(Train.index, index=Train['Title']).drop_duplicates()
    print(get_recommendations(movie_title, cosine_sim, indices))

if __name__ == '__main__':
    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename = 'logs.log',
                        level = logging.DEBUG,
                        format = LOG_FORMAT,
                        filemode = 'w')  
    path=sys.argv
    logging.info('Started fetching')
    main(path[1])
    logging.info('Fetching Done')