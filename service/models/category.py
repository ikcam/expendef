from app import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(
        db.Integer, primary_key=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    parent_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=True
    )
    name = db.Column(
        db.String(100), nullable=False
    )
    color = db.Column(
        db.String(6)
    )
    description = db.Column(
        db.Text, nullable=True
    )

    def __repr__(self):
        return '<Category %r>' % self.name
