from app import db

class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), index=True, unique=True)
    caption = db.Column(db.String(2000))
    rating = db.Column(db.Float)
    num_contests = db.Column(db.Integer, index=True)
    num_no_meme_votes = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Meme {}>'.format(self.id)