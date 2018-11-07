from flask import Flask, render_template, redirect, request, escape, sessions
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from random import randint

app = Flask(__name__)

app.config["MYSQL_HOST"] = '127.0.0.1'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'flask_test'

mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        email = escape(request.form.get("email"))
        thwart = mysql.connection.escape_string
        login_query = "SELECT * FROM flask_test.person WHERE Email=%s"
        cur.execute(login_query, (thwart(email),))
        rv = cur.fetchone()[4]

        if rv:
            return str(rv)

    return render_template('index.html')


@app.route("/existing_email")
def existing_email():
    return render_template("existing_email.html")


@app.route("/success")
def success():
    return render_template('success.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = escape(request.form.get('email'))
        username = escape(request.form.get('username'))
        password = sha256_crypt.hash(str(escape(request.form.get('password'))))

        cur = mysql.connection.cursor()
        thwart = mysql.connection.escape_string

        email_query = "SELECT Email FROM flask_test.person WHERE Email=%s"
        cur.execute(email_query, (thwart(email),))
        exis_email = cur.fetchone()

        if exis_email:
            cur.close()
            return render_template('existing_email.html')

        else:
            insert_query = "INSERT INTO flask_test.person (ID, Username, Password, Email, Balance) VALUES (NULL, %s, %s, %s, %s)"
            cur.execute(insert_query, (thwart(username), thwart(str(password)), thwart(email), randint(-392, 1000)))

            mysql.connection.commit()
            cur.close()
            return render_template('success.html')

    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        thwart = mysql.connection.escape_string

        login_query = "SELECT * FROM flask_test.person WHERE Email=%s"
        cur.execute(login_query, (thwart(email),))
        db_pass = cur.fetchone()[2]
        # beacuse of size of this site we dont care about redundant usernames

        if sha256_crypt.verify(password, db_pass):

            info_query = "SELECT * FROM flask_test.person WHERE Email=%s AND Password=%s"

            cur.execute(info_query, (thwart(email), thwart(db_pass)))

            balance = cur.fetchone()[4]

            return str(balance)

        else:
            error = "Invalid password or email"

    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
