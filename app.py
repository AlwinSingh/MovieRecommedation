import streamlit as st
import pickle
import requests
import matplotlib.pyplot as plt
import urllib

movies_pickle = pickle.load(open('movies.pkl', 'rb'))
movies_title_list = movies_pickle['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    try:
        movie_index = movies_pickle[movies_pickle['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[0:6]

        movies_recommendation_list = []
        for i in movies_list:
            movie_selected = movies_pickle.iloc[i[0]]
            movie_id = movie_selected.id
            movies_recommendation_list.append({'id': movie_id,
                                               'title':movie_selected.title,
                                               'poster':getMoviePoster(movie_id)})
        return movies_recommendation_list
    except:
        return []

def getMoviePoster(moviie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7148f5329aa7fc63de112cff89cc036f&language=en-US'.format(moviie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def renderFrontend():
    st.title('Movie Recommender System')
    selected_movie_title = st.selectbox(
        'How would you like to be contacted?',
        movies_title_list)
    if st.button('Recommend'):
        recommendations = recommend(selected_movie_title)

        if (len(recommendations) > 0):
            columns = st.columns(len(recommendations))
            for column, recommendation in zip(columns, recommendations):
                column.text(recommendation['title'])
                column.image(recommendation["poster"])
        else:
            st.write("Oops! Couldn't find any recommendations!")
            st.text("Feedback to the Developer to better train the Model!")

renderFrontend()