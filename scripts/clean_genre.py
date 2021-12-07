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

# making the dict for mapping the names of same genres
global replace_dict
replace_dict={
   "science_friction":"sci_fi",
    "sci fi":"sci_fi",
    "science friction":"sci_fi",
    "science fiction":"sci_fi",
    "sci-fi":"sci_fi",
    "amine":"animated",
    "animation":"animated",
    "cartoon":"animated",
    "tokusatsu": "animated",
    "superhero": "animated",
    "suspense": "thriller",
    "dramedy": "drama",
    "blaxploitation": "exploitation",
    "biopic": "biography",
    "bio-pic": "biography",
    "biographical": "biography",
    "kung fu": "martial_arts",
    "martial arts": "martial_arts",
    "kung fu": "martial_arts",
    "kung-fu": "martial_arts",
    "film": "",
    "neo-noir": "noir",
    "devotional": "religious",
    "children": "teen",
    "porno": "adult",
    "history": "historical",
    "rom com": "romance-comedy",
    "rom-com": "romance-comedy",
    "love": "romance",
    "periodic":"historical",
    "period":"historical",
    "football":"sports",
    "youth":'teen',
    "sexual":"adult",
    "/":" ",
    '-':' ',
    "slice of life":'slice_of_life',
    "love":"romance",
}


# for again splitting on the basics of the ','
def genre_updated(data):
    df1 = pd.DataFrame(columns = ['Release Year', 'Title', 'Origin/Ethnicity', 'Director', 'Cast','Genre', 'Wiki Page', 'Plot','Genre_1','Genre_updated','Genre_updated1'])
    for i,row in data.iterrows():
        if len(row['Genre_updated'].split(','))>1:
            for i in row['Genre_updated'].split(','):
               # print(i)
                df=pd.DataFrame(row).T
                df['Genre_updated1']=i
                df1=pd.concat([df1,df])
        else:
            df=pd.DataFrame(row).T
            df['Genre_updated1']=df['Genre_updated']
            df1=pd.concat([df1,df])
    df['Genre_updated1']=df['Genre_updated1'].apply(lambda x: x.strip())       
    return df1.reset_index(drop=True)

# for changing the genre according to final list if the genre is single then it will be the same, if it contains the approximatelly same in the choices final list then returning the list of those genres else null string
def genre_list(x):
    if x in choices_final:
        return x
    elif process.extractBests(x, choices_final,score_cutoff=80,limit=20) !=[]:
        #print(choices_final)
        a=process.extractBests(x, choices_final,score_cutoff=80,limit=20)
        #print(a)
        return ','.join([a[i][0] for i in range(len(a))])
    else:
        return ''
        

#making the list of unique qenure's and the list containing the list of approximately same genre name 
def list_prep(data,choices,li):
    for i in data:
        if i[1]==[]:
            choices.append(i[0])
        else:
            li.append(i[0])
    return choices,li

# for splitting the multiple genre on the basics of ' ,' and making the new rows
def genre(data):
    df1 = pd.DataFrame(columns = ['Release Year', 'Title', 'Origin/Ethnicity', 'Director', 'Cast','Genre', 'Wiki Page', 'Plot', 'Genre_1','Genre_updated'])
    for i,row in data.iterrows():
        if len(row['Genre_1'].split(','))>1:
            for i in row['Genre_1'].split(','):
               # print(i)
                df=pd.DataFrame(row).T
                df['Genre_updated']=i
                df1=pd.concat([df1,df])
        else:
            df=pd.DataFrame(row).T
            df['Genre_updated']=df['Genre_1']
            df1=pd.concat([df1,df])
    df['Genre_updated']=df['Genre_updated'].apply(lambda x: x.strip())
    return df1.reset_index(drop=True)



def main(df): 
    '''This is the main function of the program
    '''
    print('IN MAIN')
    #Replacing the unknown with the null string
    df['Genre_1']= df['Genre'].str.replace("unknown", "")
    #for checking the counts of each genre
    dax=df['Genre_1'].value_counts().rename_axis('Genres_1').reset_index(name='counts')
    #storing the selected top 17 genre's and saving them into a variable choices
    choices = [i for i in dax['Genres_1'].to_list() if len(i.split())<2][1:18]  
    li=[]
    print('Making List')
    #looping over the list of quenres and making the list  of unique qenure's and the list containing the list of approximately same genre name  
    for i in range(10,len(dax['Genres_1'].to_list()),10):
        inputt=dax['Genres_1'].to_list()[:i]
        data=[[i,process.extractBests(i, choices,score_cutoff=80,limit=20)] for i in inputt if i not in choices if i not in li]
        choices,li=list_prep(data,choices,li)
    print('Removing Spaces')
    # removing the extra spaces from the starting and ending
    df['Genre_1']=df['Genre_1'].apply(lambda x: x.strip())
    print('Replacing Genre')
    #replacing the the genre names
    for key,items in replace_dict.items():
        df['Genre_1']= df['Genre_1'].str.replace(key,items)
    df['Genre_1']=df['Genre_1'].apply(lambda x: x.strip())
    print('splitting the multiple genre')
    #splitting the multiple genre on the basics of ' ,' and making the new rows
    df=genre(df)
    # removing the extra space after spliting the multiple genres
    df['Genre_updated']=df['Genre_updated'].apply(lambda x: x.strip())

    #repeating the same process from taking the top 17 genres and making the list of unique genres once again and list of common genres

    dax=df['Genre_updated'].value_counts().rename_axis('Genres_updated').reset_index(name='counts')
    choices = [i for i in dax['Genres_updated'].to_list() if len(i.split())<2][1:18]
    li=[]

    # for slecting the single genres
    for i in range(10,len(dax['Genres_updated'].to_list()),10):
        inputt=dax['Genres_updated'].to_list()[:i]
        data=[[i,process.extractBests(i, choices,score_cutoff=80,limit=20)] for i in inputt if i not in choices if i not in li]
        choices,li=list_prep(data,choices,li)
    print('final_list')
    # making the final list of genres
    global choices_final
    choices_final=[row['Genres_updated'] for i,row in dax.iterrows() if row['Genres_updated'] in choices if row['counts']>30]

    # changing the genre according to final list if the genre is single then it will be the same, if it contains the approximatelly same in the choices final list then returning the list of those genres else null string
    df['Genre_updated']=df['Genre_updated'].apply(lambda x: genre_list(x))
    print('Splitting on the basis of " , "')
    #splitting multiple genres on the basics of ' , '
    new_df=genre_updated(df)
    #saving the updated dataframe into csv
    new_df.drop_duplicates().drop(['Genre_1','Genre_updated'],axis=1).rename(columns={'Genre_updated1': 'Genre_updated'}).to_csv('wiki_movie_plots_deduped_cleaned_genre_script.csv',index=False)
    

if __name__ == '__main__':
    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename = 'logs_genre.log',
                        level = logging.DEBUG,
                        format = LOG_FORMAT,
                        filemode = 'w')  

    path=sys.argv
    logging.info('Started fetching')
    main(pd.read_csv(path[1]))
    logging.info('Fetching Done')
         