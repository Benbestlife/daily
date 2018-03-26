from flask import Flask, redirect, url_for, jsonify, request

app = Flask(__name__)
users = []


@app.route("/", methods=["GET"])
def index():
    return'''<form method=post action='/add'>
    <input type=text name=author>
    <button>提交</button>
    </form>
    '''


@app.route("/add", methods=["POST"])
def add():
    form = request.form
    users.append(dict(author=form.get("author", "")))
    return redirect(url_for(".index"))


@app.route("/json")
def json():
    return jsonify(users)


app.run()
