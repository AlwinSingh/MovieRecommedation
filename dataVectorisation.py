from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

def dataVectorisation(movies_metadata_compact):
    print("[Step 3] Vectorising data...", datetime.now().strftime("%H:%M:%S"))
    # Start of Text Vectorisation
    # We will now compare the 'tags' between Movies to determine the Movie Similarity
    # However, rather than calculating the number of same/similar words, we use VECTORISATION which is highly efficient
    # Text Vectorisation: https://openreview.net/pdf?id=HylJtiRqYQ
    # Text Vectorisation: https://www.youtube.com/watch?v=1xtrIEwY_zY&t=1s&ab_channel=CampusX @ 59 Minutes
    cv = CountVectorizer(max_features=30000,stop_words='english')
    vectors = cv.fit_transform(movies_metadata_compact['tags']).toarray()

    # We have roughly 13,000 vector points to plot. Rather than using Euclidean distance
    # to measure how similar / not similar a movie is, we will use Cosine Distance (Angle)
    # The larger the vector dataset, the worse it is to use Euclidean distance
    # For example, if the Angle difference between 2 Vectors is 5 degrees, it means they are similar
    # However, if the Angle difference between 2 Vectors is 90 degees, it means they are very different
    similarityCosineMatrix = cosine_similarity(vectors)

    print("[Step 3] Vectorising data complete...", datetime.now().strftime("%H:%M:%S"))
    return similarityCosineMatrix