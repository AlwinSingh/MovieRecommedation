import numpy as np
import pandas as pd
import ast
import nltk
from nltk.stem.porter import PorterStemmer
from datetime import datetime

# Data Pre-processing

# To stem the words using NLTK
ps = PorterStemmer()

# Fn to Extract tuple data into a List as String
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

# Fn to Extract 3 tuples of data into a List as String
def convertFirst3Actors(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if (counter != 3):
            L.append(i['name'])
            counter+=1
        else:
            break
    return L

# Fn to Extract just the Director data into a List as String
def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

# Fn to Stem the words for TEXT VISUALISATION
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def dataPreProcessing(movies_metadata):
    print("[Step 2] Preprocessing data...", datetime.now().strftime("%H:%M:%S"))
    # Part A: Extract genres into a list
    movies_metadata['genres'] = movies_metadata['genres'].apply(convert)

    # Part B: Extract keywords into a list
    movies_metadata['keywords'] = movies_metadata['keywords'].apply(convert)

    # Part C: Extract top 3 cast actors into a list
    movies_metadata['cast'] = movies_metadata['cast'].apply(convertFirst3Actors)

    # Part D: Extract only the DIRECTOR from crew into a list
    movies_metadata['crew'] = movies_metadata['crew'].apply(fetch_director)

    # Part E: Extract overview into a list
    movies_metadata['overview'] = movies_metadata['overview'].apply(lambda x:x.split())

    # Part F: Remove spacing from the Strings in the lists
        # Now we must remove spaces in the Strings in the lists so that the recommender
        # system doesn't confuse 'Sam Depp' and 'Sam Morton' to be interpreted as
        # 'Sam','Depp','Morton' which will throw off the recommendations
        # The system should interpret it as 'SamDepp','SamMorton'
    movies_metadata['genres'] = movies_metadata['genres'].apply(lambda x:[i.replace(" ","") for i in x])
    movies_metadata['keywords'] = movies_metadata['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
    movies_metadata['cast'] = movies_metadata['cast'].apply(lambda x:[i.replace(" ","") for i in x])
    movies_metadata['crew'] = movies_metadata['crew'].apply(lambda x:[i.replace(" ","") for i in x])

    # Part G: Create a new TAG Column that contains genres,keywords,cast and crew in LOWER CASE
        # Note: We use .copy to prevent SettingWithCopyWarning: https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
    movies_metadata['tags'] = movies_metadata['overview'] + movies_metadata['genres'] + movies_metadata['keywords']\
                              + movies_metadata['cast'] + movies_metadata['crew']
    movies_metadata_compact = movies_metadata.copy(deep=False)
    movies_metadata_compact = movies_metadata_compact[['id','title','tags']]
    movies_metadata_compact['tags'] = movies_metadata_compact['tags'].apply(lambda x:" ".join(x))
    movies_metadata_compact['tags'] = movies_metadata_compact['tags'].apply(lambda x:x.lower())

    # Part H: As part of TEXT VECTORISATION, we need to remove certain similar words
        # such as [Love, Loved, Loving] all mean the same thing and will be counted as part
        # of Text Vectorisation which can throw off the recommender system
    # We will use NLTK (Natural Language Processing) to fix this issue in the tags dataset
    # NLTK will convert [Loved,Loving,Love] into [Love]
    # More info: https://www.nltk.org/howto/stem.html
    movies_metadata_compact['tags'] = movies_metadata_compact['tags'].apply(stem)

    # End of data pre-processing
    print("[Step 2] Preprocessing data complete...", datetime.now().strftime("%H:%M:%S"))
    return movies_metadata_compact