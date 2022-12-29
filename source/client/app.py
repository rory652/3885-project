from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
def hello_world():
    r = requests.post("http://api:5000/login", json={"username": "ronald", "password": "woman slayer", "permissions": 4})
    if "Set-Cookie" in r.headers:
        return render_template("index.html", cookies=r.headers["Set-Cookie"], body=r.text)
    elif "Set-Cookies" in r.headers:
        return render_template("index.html", cookies=r.headers["Set-Cookies"], body=r.text)

    return render_template("index.html", cookies="none", body=r.text)
