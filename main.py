from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
@cross_origin() 
def root():
    return render_template('index.html')


@app.route("/api/submit-link", methods = ['POST'])
@cross_origin()
def link():
    print("LINK CLICKED")
    url = request.form['url']
    title = request.form['title']

    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    contents = soup.find()
    content_text = contents.get_text()

    return render_template('content.html', data={"content" : url, "raw_text": content_text})
    # return render_template('content.html')

# @app.route("/")
# def hello():
#     return "<h1 style='color:black'>FLASK SERVER</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
