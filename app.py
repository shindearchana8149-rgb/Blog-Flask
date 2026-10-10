from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app=Flask(__name__)
DB="blog.db"

def db():
    con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
    con.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY,title TEXT,content TEXT)")
    con.commit(); return con

@app.route("/")
def index():
    con=db(); posts=con.execute("SELECT * FROM posts ORDER BY id DESC").fetchall(); con.close()
    return render_template("index.html",posts=posts)

@app.route("/new",methods=["GET","POST"])
def new():
    if request.method=="POST":
        con=db(); con.execute("INSERT INTO posts(title,content) VALUES(?,?)",
          (request.form["title"],request.form["content"])); con.commit(); con.close()
        return redirect(url_for("index"))
    return render_template("new.html")

@app.route("/delete/<int:id>",methods=["POST"])
def delete(id):
    con=db(); con.execute("DELETE FROM posts WHERE id=?",(id,)); con.commit(); con.close()
    return redirect(url_for("index"))

if __name__=="__main__": app.run(debug=True)
