from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=['post', 'get'])
def home():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        r = requests.post("http://api:5000/login", json={"username": username, "password": password})
        if "Set-Cookie" in r.headers:
            return render_template("index.html", cookies=r.headers["Set-Cookie"], body=r.text)
        elif "Set-Cookies" in r.headers:
            return render_template("index.html", cookies=r.headers["Set-Cookies"], body=r.text)
        return render_template("index.html", cookies="none", body=r.text)

    return render_template("index.html")
