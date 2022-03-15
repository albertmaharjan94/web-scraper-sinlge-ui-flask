from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import psycopg2


app = Flask(__name__)

conn = psycopg2.connect(
        host="45.115.217.102",
        database="scrap_db",
        user="postgres",
        password="postgres")


@app.route("/")
@cross_origin() 
def root():
    return render_template('index.html')

@app.route("/api/save-data", methods = ['POST'])
@cross_origin()
def saveLink():

    title = request.form['title']
    ip = request.form['ip']
    link = request.form['link']
    without_tag = request.form['without_tag']
    with_tag = request.form['with_tag']
    
    cur = conn.cursor()
    try:

        cur.execute('INSERT INTO data_dump (title, link, without_tag, with_tag, ip_address)'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (title,
                    link,
                    str(without_tag),
                    str(with_tag), 
                    ip)
                    )

        conn.commit()

    except Exception as e:
        cur.close()
        return jsonify({"success" : False, "msg": "Something went wrong."})

    return jsonify({"success" : True, "msg": "Saved successfully", "data": {
        "title" : title,
        "ip" : ip,
        "link" : link,
        "without_tag" : without_tag,
        "with_tag" : with_tag,
    }})

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
    return render_template('content.html', data={"content" : url, "raw_text": content_text, "title": title, "raw_data": contents})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
