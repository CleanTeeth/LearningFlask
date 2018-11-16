from flask import Flask, render_template, redirect, request, escape, session, url_for
from models import db, User
from passlib.hash import sha256_crypt
from random import randint


app = Flask(__name__)

app.config.update(
    SECRET_KEY='bf9d247b9d724be9858ca84d326cb77c',
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI="mysql://root:@localhost/sqlalchemy",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.init_app(app)


@app.route('/ignore')
def setting_sessions():
    session['block'] = True
    return redirect(url_for('index'))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        email = request.form.get('email')

        info_count = User.query.filter_by(email=email).count()

        if info_count > 0:
            balance = [r.balance for r in db.session.query(User.balance).filter_by(email=email)]
            return render_template('index_text.html', balance=int(balance[0]))

    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        session['log_in'] = False
        email = request.form.get('email')
        username = escape(request.form.get('username'))
        password = sha256_crypt.hash(str(escape(request.form.get('password'))))

        exis_email = User.query.filter_by(email=str(email)).count()

        if exis_email > 0:
            return render_template('existing_email.html')

        else:
            user = User(username, email, randint(-392, 1000), password)
            db.session.add(user)
            db.session.commit()

            return render_template('success.html')

    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db_pass = [r.password for r in db.session.query(User.password).filter_by(email=email)]

        if sha256_crypt.verify(password, db_pass[0]):
            balance = [r.balance for r in db.session.query(User.balance).filter_by(email=email)]
            username = [r.username for r in db.session.query(User.username).filter_by(email=email)]
            session['balance'] = int(balance[0])
            session['username'] = str(username[0])
            return redirect(url_for('user_dashboard'))

        else:
            error = "Invalid password or email"

    return render_template('login.html', error=error)


@app.route('/user_dashboard')
def user_dashboard():
    if 'log_in' in session:
        return render_template('user_dashboard.html', balance=session.get('balance', None), username=session.get('username', None))

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'block' in session:
        session.pop('log_in', None)
        return redirect(url_for('index'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
