from app import app, db
from app.models import Meme

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Meme': Meme}