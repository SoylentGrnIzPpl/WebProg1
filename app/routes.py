from flask import render_template, request, redirect, url_for, make_response, session, flash
from app import app, db
from app.forms import LoginForm
from app.models import User



@app.route("/")
@app.route("/home")
def get_index():
    # username = request.cookies.get("username", None)
    if 'username' in session:
        username = session['username']
    else: 
        return redirect(url_for("get_login"))
    return render_template('home.html', name=username)

@app.route("/other")
def get_other():
    # username = request.cookies.get("username", None)
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for("get_login"))
    return render_template('other.html', name = username)

# @app.route("/hello")
# def get_hello():
#     return render_template('hello.html', name="Santa")

# @app.route("/hi")
# @app.route("/hi/<name>")
# def get_hi(name="Dick"):
#     name = name[::-1]
#     return render_template('hello.html', name=name)

@app.route("/login", methods=['GET'])
def get_login():
    # username = request.cookies.get("username", None)
    if 'username' in session:
        return redirect(url_for("get_index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('get_index'))
    return render_template('login.html', title='Login', form=form)

@app.route("/login", methods=['POST'])
def post_login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    # response = make_response(redirect(url_for('get_index')))
    # response.set_cookie("username", username)
    if username != None and password != None:
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        session['username'] = username
        return redirect(url_for('get_index'))
    else:
        flash('Username and Password fields must be filled.')
        return redirect(url_for('get_login'))
    # password = request.form.get("password", "<missing password>")
    # if password == "pass":
    #     return redirect(url_for('get_hi', name=username))
    # else:
    # return response

@app.route("/logout", methods=['GET'])
def get_logout():
    # response = make_response(redirect(url_for('get_login')))
    # response.delete_cookie("username")
    session.pop('username')
    return redirect(url_for('get_login'))
    # return response

@app.route("/register", methods=['GET'])
def get_register():
    if 'username' in session:
        return redirect(url_for("get_index"))
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def post_register():

    username = request.form.get("username", None)

    if(request.form.get("password", None) == request.form.get("repPassword", None)):
        password = request.form.get("password")
    else:
        password = None

    if username != None and password != None:
        session['username'] = username
        user = User(username = username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')
    else:
        return redirect(url_for('get_register'))
    return redirect(url_for('get_index'))

