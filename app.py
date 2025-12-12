from flask import Flask,render_template,request,session
import sqlite3

def get_db():
    conn = sqlite3.connect("fakeNewsUpdated.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)


app.secret_key = "tappin'it"



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/randomArticle", methods=["GET"])
def randomArticle():
    conn = get_db()
    article = conn.execute("SELECT * FROM fakenews ORDER BY RANDOM() LIMIT 1").fetchone()
    article = dict(article)
    conn.close()
    print (article)
    content = article['content']
    validity = article['realOrFake']
    print(content)
    return render_template("article.html", article=content,validity=validity)

@app.route("/guesser", methods=["GET", "POST"])
def guesser():
    conn = get_db()

    if "score" not in session:
        session["score"] = 0

    if "highscore" not in session:
        session["highscore"] = 0

    if request.form.get("Real") == "Real":

        validity = session.get("validity")
        content = session.get("content")

        if validity == "True":
            session["score"] += 1
            return render_template("result.html", article=content,validity="Correct! It is Real.", score=session["score"], highscore=session.get("highscore",0))

        else:
            if session["score"] > session["highscore"]:
                session["highscore"] = session["score"]
            session["score"] = 0
            return render_template("result.html", article=content,validity="Wrong! It is Fake.", score=session["score"], highscore=session["highscore"])

    if request.form.get("Fake") == "Fake":
        validity = session.get("validity")
        content = session.get("content")

        if validity == "Fake":
            session["score"] += 1
            return render_template("result.html", article=content,validity="Correct! It is Fake.", score=session["score"], highscore=session.get("highscore",0))
        else:
            if session["score"] > session["highscore"]:
                session["highscore"] = session["score"]
            session["score"] = 0
            return render_template("result.html", article=content,validity="Wrong! It is Real.", score=session["score"],highscore=session.get("highscore",0))

    article = conn.execute("SELECT * FROM fakenews ORDER BY RANDOM() LIMIT 1").fetchone()
    article = dict(article)
    conn.close()
    print (article)
    content = article['content']
    validity = article['realOrFake']
    print(content)

    session["validity"] = validity
    session["content"] = content

    return render_template("guesser.html", article=content,validity="", score=session["score"],highscore=session.get("highscore",0))



if __name__ == "__main__":
    app.run(debug=True)