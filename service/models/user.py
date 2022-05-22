from app import db
from passlib.hash import pbkdf2_sha256
from passlib.pwd import genword


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer, primary_key=True
    )
    email = db.Column(
        db.String(120), unique=True, nullable=False
    )
    password = db.Column(
        db.String(120), nullable=False
    )
    is_active = db.Column(
        db.Boolean, default=True, nullable=False
    )
    is_superuser = db.Column(
        db.Boolean, default=False
    )
    first_name = db.Column(
        db.String(100), nullable=False
    )
    last_name = db.Column(
        db.String(100), nullable=False
    )
    date_creation = db.Column(
        db.DateTime, default=db.func.now(), nullable=False
    )
    last_login = db.Column(
        db.DateTime, nullable=True
    )

    def __repr__(self):
        return '<User %r>' % self.email

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    @classmethod
    def make_password(self, length=12):
        return genword(length=length)
