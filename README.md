# MoviesRecommender
A content-based movie recommendation system built using Python with Machine Learning

To run the project you must first download the Data Files to train the model - https://drive.google.com/file/d/1gRQbAV9fhrglwSlIU1kLJVUd3Ja6tV7U/view?usp=sharing

Subsequently, open the project and install the necessary modules through pip.
The movies recommendation system is served through StreamLit a frontend framework for python projects. 
To start the streamlit web app, run the following command: streamlit run app.py

Alternatively, you may also use the APIs file in Api.js which you have to run it like any other standalone python file.

Web Application Demonstration:
https://user-images.githubusercontent.com/62194353/197988737-5827dfb5-938f-4722-9285-07e4c42a6bde.mp4

API Demonstration:
https://user-images.githubusercontent.com/62194353/197988954-f89d7c01-60b9-46de-9ad0-632e1037f4e8.mp4


Differences in types of Recommender System Approachhes
Content Based Approach -> Recommends based on the similarity of content you watch/view/etc [Chosen for this project]

Collab Filtering Approach -> Based on user's interests. Example if Person A and B watches Movie X and loves it, if Person B watches Movie Z then A also gets recommended it. This usually applies to social media such as liking user's posts, etc

Hybrid -> Mixture of both
