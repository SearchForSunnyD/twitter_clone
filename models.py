from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

pass_hash = generate_password_hash


def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model for twitter clone"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
        doc="Unique username.",
    )
    password = db.Column(db.Text, nullable=False, doc="User hashed password")
    email = db.Column(
        db.String(50), nullable=False, unique=True, doc="Unique email to link to user."
    )
    first_name = db.Column(db.String(30), nullable=False, doc="User first name.")
    last_name = db.Column(db.String(30), nullable=False, doc="User last name.")

    feedbacks = db.relationship(
        "Feedback", backref="users", cascade="all, delete-orphan"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def feedback(self):
        return [feedback.serialize_info() for feedback in self.feedbacks]

    def serialize_info(user):
        """Serialize this objects data into a JSON readable format"""
        return {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
        }

    def check_password(self, pass_to_check):
        return check_password_hash(self.password, pass_to_check)


class Feedback(db.Model):
    """Feedback on a user"""

    __tablename__ = "feedback"

    id = db.Column(
        db.Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        doc="Unique ID",
    )
    title = db.Column(db.String(100), nullable=False, doc="Feedback title")
    content = db.Column(db.Text, nullable=False, doc="Feedback content")
    username = db.Column(
        db.String(20),
        db.ForeignKey("users.username"),
        nullable=False,
        doc="Linked user",
    )

    def serialize_info(info):
        """Serialize this objects data into a JSON readable format"""
        return {
            "id": info.id,
            "title": info.title,
            "content": info.content,
            "username": info.username,
        }
