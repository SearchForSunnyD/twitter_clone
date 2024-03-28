from flask import Flask, render_template, redirect, session, request
from models import db, connect_db, User, Feedback, pass_hash

from forms import RegisterUserForm, LoginUserForm, FeedbackForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///twitter_clone"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

app.secret_key = "super_secret"

connect_db(app)
with app.app_context():
    db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 page."""
    return render_template("404.html"), 404


@app.route("/")
def home():
    """
    Redirect to register.
    """
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def handle_register():
    """
    Show register form.
    """
    form = RegisterUserForm()
    if form.validate_on_submit():
        new_user = User()
        for field in form:
            if field.name == "password":
                setattr(new_user, field.name, pass_hash(field.data))
            else:
                setattr(new_user, field.name, field.data)
        db.session.add(new_user)
        db.session.commit()

        session["user"] = new_user.serialize_info()

        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("reg_form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def handle_login():
    """
    Show login form.
    """
    form = LoginUserForm()
    if form.validate_on_submit():
        try:
            user = User().query.get_or_404(request.form["username"])
        except:
            return redirect("/")
        if user.check_password(request.form["password"]) == True:
            session["user"] = user.serialize_info()

            return redirect(f"/users/{user.username}")
        else:
            return redirect("/")
    else:
        return render_template("login_form.html", form=form)


@app.route("/logout", methods=["GET"])
def handle_logout():
    """
    Logout current user.
    """
    session["user"] = ""

    return redirect("/")


@app.route("/users/<username>")
def show_the_secret(username):
    """
    Display the users page.
    """
    user = User().query.get_or_404(username)
    if session["user"]:
        try:
            feedback = user.feedback
        except:
            feedback = []
        return render_template(
            "user.html", feedback=feedback, user=user.serialize_info()
        )
    else:
        return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    if username == session["user"].username:
        redirect("/")
    User().query.get_or_404(username)
    form = FeedbackForm()
    if form.validate_on_submit():
        new_feedback = Feedback(username=username)
        for field in form:
            setattr(new_feedback, field.name, field.data)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f"/users/{username}")
    else:
        return render_template("feedb_form.html", form=form)


@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    feedback = Feedback().query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    if feedback.username == session["user"].username:
        redirect("/")
    if form.validate_on_submit():
        data = form.data
        data.pop("csrf_token")
        for field in form:
            setattr(feedback, field.name, field.data)
        db.session.commit()
        return redirect(f"/feedback/{feedback.username}/{feedback.id}")
    else:
        return render_template("feedb_form.html", form=form)


@app.route("/feedback/<feedback_id>/delete", methods=["GET", "POST"])
def delete_feedback(feedback_id):
    feedback = Feedback().query.get_or_404(feedback_id)
    username = feedback.username
    if username == session["user"].username:
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f"/users/{username}")


@app.route("/users/<username>/delete", methods=["GET", "POST"])
def delete_user(username):
    user = User().query.get_or_404(username)
    if user.username == session["user"]["username"]:
        db.session.delete(user)
        db.session.commit()
        session["user"] = ""
    return redirect(f"/")
