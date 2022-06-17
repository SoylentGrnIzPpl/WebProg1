from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)

@app.route("/")
def get_index():
    return "<p>Hello from flask :)</p>"

@app.route("/hello")
def get_hello():
    return render_template('hello.html', name="Santa")

@app.route("/hi")
@app.route("/hi/<name>")
def get_hi(name="Dick"):
    name = name[::-1]
    return render_template('hello.html', name=name)

@app.route("/login", methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def post_login():
    username = request.form.get("username", "<missing username>")
    password = request.form.get("password", "<missing password>")
    if password == "pass":
        return redirect(url_for('get_hi', name=username))
    else:
        return redirect(url_for('get_login'))
