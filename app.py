from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"

app.config["MONGO_URI"] = "mongodb+srv://root:1234@atlascluster.h5phasl.mongodb.net/test"
mongo = PyMongo(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Requests: username, password 가져와서 and username, password라는 variable 에 저장
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # using find_one(), assign the found user to 'user' variable
        user = mongo.db.uesrs.find_one({'username': username})
        print(user)

        # if user and check_password_hash(user['username'], password):
        if user and (user['password']==password):
            #login
            session["username"] = username
            print(session)
            return redirect(url_for("dashboard"))

        else:
            print("Invalid username")

    return render_template("login.html")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/dashboard')
def dashboard():
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.uesrs.find_one({'username' : username})

        if user:
             print("Username already exists")
        else:
            # hashed_password = generate_password_hash(password)
            mongo.db.users.insert_one({'username': username, 'password': password})

        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
