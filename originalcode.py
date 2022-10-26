import numpy as np
import pandas as pd

movies_metadata = pd.read_csv('movies_metadata.csv', low_memory=False)
keywords_metadata = pd.read_csv('keywords.csv', low_memory=False)
credits_metadata = pd.read_csv('credits.csv', low_memory=False)

movies_metadata.id = movies_metadata.id.astype(str)
keywords_metadata.id = keywords_metadata.id.astype(str)
credits_metadata.id = credits_metadata.id.astype(str)

movies_metadata = movies_metadata.merge(keywords_metadata,
                                        how='inner',
                                        on='id')

movies_metadata = movies_metadata.merge(credits_metadata,
                                        how='inner',
                                        on='id')

movies_metadata = movies_metadata[['id','title','overview','genres','keywords','cast','crew']]
movies_metadata.id = pd.to_numeric(movies_metadata.id, errors="coerce")
movies_metadata = pd.DataFrame(movies_metadata)

# Remove empty / null data
movies_metadata.dropna(inplace=True)
print("Null values ", movies_metadata.isnull().sum())
print("\n")

# Cleaning of Data;
df = movies_metadata
df = df[df['keywords'].map(lambda d: len(d)) > 2]
df = df[df['genres'].map(lambda d: len(d)) > 2]
df = df[df['cast'].map(lambda d: len(d)) > 2]
movies_metadata = df;

# Check for Duplicates
movies_metadata.drop_duplicates(inplace=True)
print("Duplicate values ", movies_metadata.duplicated().sum())
print("\n")

# Data Pre-processing
import ast
# Extract tuple data into a List as String
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
# Part A: Extract genres into a list
movies_metadata['genres'] = movies_metadata['genres'].apply(convert)

# Part B: Extract keywords into a list
movies_metadata['keywords'] = movies_metadata['keywords'].apply(convert)

# Part C: Extract top 3 cast actors into a list
# Extract tuple data into a List as String
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
movies_metadata['cast'] = movies_metadata['cast'].apply(convertFirst3Actors)

# Part D: Extract only the DIRECTOR from crew into a list
def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L
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
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
movies_metadata_compact['tags'] = movies_metadata_compact['tags'].apply(stem)

# End of data pre-processing

# Start of Text Vectorisation
# We will now compare the 'tags' between Movies to determine the Movie Similarity
# However, rather than calculating the number of same/similar words, we use VECTORISATION which is highly efficient
# Text Vectorisation: https://openreview.net/pdf?id=HylJtiRqYQ
# Text Vectorisation: https://www.youtube.com/watch?v=1xtrIEwY_zY&t=1s&ab_channel=CampusX @ 59 Minutes
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=30000,stop_words='english')
vectors = cv.fit_transform(movies_metadata_compact['tags']).toarray()

# We have roughly 13,000 vector points to plot. Rather than using Euclidean distance
# to measure how similar / not similar a movie is, we will use Cosine Distance (Angle)
# The larger the vector dataset, the worse it is to use Euclidean distance
# For example, if the Angle difference between 2 Vectors is 5 degrees, it means they are similar
# However, if the Angle difference between 2 Vectors is 90 degees, it means they are very different
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

# Pickle is used for our web app, it basically helps us to convert all the data of the Titles into an Array/List
# Rather than executing the entire code again
# We expore the Similarity & Movie Metadata File for our WebApp
import pickle
pickle.dump(movies_metadata,open('movies.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))

# Recommend top 5 movies based on Cosine Distance (Angle) of all 13,000 Vectors sorted in Descending Order
def recommend(movie):
    movie_index = movies_metadata_compact[movies_metadata_compact['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    movies_recommendation_list = []
    for i in movies_list:
        movies_recommendation_list.append({'id':movies_metadata_compact.iloc[i[0]].id,
                                           'title':movies_metadata_compact.iloc[i[0]].title})
    return movies_recommendation_list

print(recommend('Toy Story'))