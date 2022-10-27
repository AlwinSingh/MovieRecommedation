# :movie_camera: MoviesRecommender
A content-based movie recommendation system built using Python with Machine Learning.

* The CSV data files used have roughly 13,000 movies which is then translated into a 2D Matrix with 5000 data points. The reason for this is because we plot vector points to determine which movies are the most relevant through Cosine Rule (Angle between each movie plotted on an X & Y Axis aka a Graph lol).

## Project setup
1) Download the Data Files to train the model - https://drive.google.com/file/d/1gRQbAV9fhrglwSlIU1kLJVUd3Ja6tV7U/view?usp=sharing
2) Drag the data files to the project root directory
3) Open the project and run pip install.
4) Install any missing modules / dependencies if any

## Run the project
1) The movies recommendation system is served through StreamLit a frontend framework for python projects. 
2) Start the streamlit web app with 'streamlit run app.py'
3) Note: Streamlit web app relies on extracting data from the CSV rather than the APIs which exist in Api.js

## [Optional] Run the API
1) Right click on api.py and run it like any other standalone python file.
2) The start up time for api.py is slow as it loads & builds up the data sets

## :globe_with_meridians: Web Application Demonstration:

https://user-images.githubusercontent.com/62194353/197988737-5827dfb5-938f-4722-9285-07e4c42a6bde.mp4

## :rocket: API Demonstration:

https://user-images.githubusercontent.com/62194353/197988954-f89d7c01-60b9-46de-9ad0-632e1037f4e8.mp4


## Recommender system filter approaches
* Content Based Approach -> Recommends based on the similarity of content you watch/view/etc [Chosen for this project because it is the most relevant for our use case where by a user inputs a movie name]

* Collab Filtering Approach -> Based on user's interests. Example if Person A and B watches Movie X and loves it, if Person B watches Movie Z then A also gets recommended it. This usually applies to social media such as liking user's posts, etc

* Hybrid -> Simply a mixture of both
