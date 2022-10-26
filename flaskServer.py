from flask import Flask,Response,jsonify,request
from mainExecutor import onStartUp, getRecommendation

app = Flask(__name__)

@app.route("/getRecommendation", methods=['GET'])
def get_recommendation():
    movie_title = request.args.get('title')
    recommendationsList = getRecommendation(movie_title)

    for movie in recommendationsList:
        print(movie)

    return jsonify({'recommendations':recommendationsList})

if __name__ == '__main__':
    onStartUp()
    app.run(debug=True)