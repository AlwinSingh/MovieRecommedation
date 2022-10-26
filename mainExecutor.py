from dataInitialiser import initialiseAndCleanseData;
from dataProcessor import dataPreProcessing;
from dataVectorisation import dataVectorisation;

#movies_metadata = None; #Returned by dataInitialiser
#movies_metadata_compact = None; #Returned by dataProcessor
#similarityCosineMatrix = None; #Returned by dataVectorisation

#Run on Flask Start Up
def onStartUp():
    global startup_success
    global movies_metadata
    global movies_metadata_compact
    global similarityCosineMatrix

    # Run dataInitaliser
    movies_metadata = initialiseAndCleanseData()
    # Run dataProcessor
    movies_metadata_compact = dataPreProcessing(movies_metadata)
    # Run dataVectorisation
    similarityCosineMatrix = dataVectorisation(movies_metadata_compact)
    startup_success = True

# Run everytime an API is called
# Recommend top 5 movies based on Cosine Distance (Angle) of all 13,000 Vectors sorted in Descending Order
def getRecommendation(movieTitle):
    global startup_success
    global movies_metadata
    global movies_metadata_compact
    global similarityCosineMatrix

    if startup_success:
        try:
            movie_index = movies_metadata_compact[movies_metadata_compact['title'] == movieTitle].index[0]
            distances = similarityCosineMatrix[movie_index]
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
            movies_recommendation_list = []
            movies_recommendation_list.append({'id': int(movies_metadata_compact.iloc[movie_index].id),
                                                'title': movies_metadata_compact.iloc[movie_index].title})
            for i in movies_list:
                movies_recommendation_list.append({'id': int(movies_metadata_compact.iloc[i[0]].id),
                                                    'title': movies_metadata_compact.iloc[i[0]].title})
            print("Movies recommendations\n", movies_recommendation_list)
            return movies_recommendation_list
        except:
            return []
    else:
        print("Start up is not successful")
        return []