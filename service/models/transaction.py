from app import db


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(
        db.Integer, primary_key=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    date_creation = db.Column(
        db.DateTime, default=db.func.now(), nullable=False
    )
    date_modification = db.Column(
        db.DateTime, default=db.func.now(), nullable=False,
        onupdate=db.func.now(),
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=False
    )
    date = db.Column(
        db.DateTime, nullable=False
    )
    description = db.Column(
        db.Text, nullable=True
    )
    is_income = db.Column(
        db.Boolean, default=False, nullable=False
    )
    amount = db.Column(
        db.Numeric(10, 2), nullable=False
    )

    def __repr__(self):
        return '<Movement %r>' % self.description
