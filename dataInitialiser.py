import numpy as np
import pandas as pd
from datetime import datetime

def initialiseAndCleanseData():
    print("[Step 1] Initialising data...", datetime.now().strftime("%H:%M:%S"))
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
    #print("Null values ", movies_metadata.isnull().sum())
    #print("\n")

    # Cleaning of Data;
    df = movies_metadata
    df = df[df['keywords'].map(lambda d: len(d)) > 2]
    df = df[df['genres'].map(lambda d: len(d)) > 2]
    df = df[df['cast'].map(lambda d: len(d)) > 2]
    movies_metadata = df;

    # Check for Duplicates
    movies_metadata.drop_duplicates(inplace=True)

    print("[Step 1] Initialising data complete...", datetime.now().strftime("%H:%M:%S"))
    return movies_metadata