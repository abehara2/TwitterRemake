from flask import Flask
from flask import render_template, jsonify, request

app = Flask(__name__)
class Tweet:
    def __init__(self, likes, content,retweets,username):
        self.likes = likes
        self.content = content
        self.retweets = retweets
        self.username = username

    def to_dict(self):
        response = {}
        response["likes"] = self.likes
        response["content"] = self.content
        response["retweets"] = self.retweets
        response["username"] = self.username
        return response

tweets = {} #maps id -> Tweet Object
current_id = 0;

def create_response(data, status, message):
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status

@app.route('/')
def index():
    global tweets
    return "Twitter"


@app.route('/posts', methods=['POST'])
def add_tweet():
    global tweets
    global current_id
    data = request.form
    likes = data.get("likes")
    content = data.get("content")
    retweets = data.get("retweets")
    username = data.get("username")
    
    tweet = Tweet(likes,content,retweets,username)
    tweets[current_id] = tweet
    current_id += 1

    return create_response(tweet.to_dict(), 200, "Tweet Posted")
    
@app.route('/posts', methods=['GET'])
def get_tweet():
    global tweets
    tweetList = [tweet.to_dict() for tweet in tweets.values()]
    response = {
        "tweets": tweetList
    }
    return create_response(response, 200, "Tweets")

@app.route('/posts/<id>', methods=['GET'])
def get_tweetByID(id):
    global tweets
    if int(id) in tweets:
        return create_response(tweets[int(id)].to_dict(), 200, "OK")
    return create_response(tweets.get(int(id)), 404, "Tweet not found")
    
@app.route('/posts/<id>/like', methods = ['POST'])
def likeTweet(id):
    global tweets
    if int(id) in tweets:
        tweet = tweets[int(id)]
        like = tweet.likes
        newLike = int(like) + 1
        tweet.likes = str(newLike)
        return create_response(tweets[int(id)].to_dict(), 200,"Tweet Liked")
    return create_response(tweets.get(int(id)), 404, "Tweet not found")

@app.route('/posts/<id>/retweet', methods = ['POST'])
def retweetTweet(id):
    global tweets
    if int(id) in tweets:
        tweet = tweets[int(id)]
        rt = tweet.retweets
        newRT = int(rt) + 1
        tweet.retweets = str(newRT)
        return create_response(tweets[int(id)].to_dict(), 200,"Tweet Retweeted")
    return create_response(tweets.get(int(id)), 404, "Tweet not found")

@app.route('/posts/<id>/delete', methods = ['POST'])
def deleteTweet(id):
    global tweets
    if int(id) in tweets:
        tweets.pop(int(id))
        return create_response(tweets[int(id)].to_dict(), 200, "Tweet Deleted")
    return create_response(tweets.get(int(id)), 404, "Tweet not found")

if __name__ == '__main__':
    app.run(debug = True)
