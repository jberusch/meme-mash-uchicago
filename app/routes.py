# local imports
from app import app, db
from app.models import Meme

# library imports
from PIL import Image
from io import BytesIO
from sqlalchemy import desc
from random import randrange
from flask import render_template, request

@app.route('/')
@app.route('/index')
def index():
    # get meme db entry
    all_memes = Meme.query.all()

    # TODO: get random indices in memes
    num_memes = len(all_memes)
    meme1_index = randrange(num_memes - 1)
    meme2_index = randrange(num_memes - 1)
    # make sure memes are different
    while meme2_index == meme1_index:
        meme2_index = randrange(num_memes - 1)

    memes = []
    memes.append(all_memes[meme1_index])
    memes.append(all_memes[meme2_index])

    # get meme sizes
    img_sizes = []
    for meme in memes:
        with open('app/static/memes/{}'.format(meme.filename), 'rb') as fp:
            img_bytes = BytesIO(fp.read())
            img = Image.open(img_bytes)
            size = img.size
            ratio = size[0] / size[1]

            # TODO: adjust these sizes later

            adjusted_size = (800, 600)
            img_sizes.append(adjusted_size)
            
    # get selection
    chosen_meme_id = request.args.get('choice')
    # if user made a choice, update the scores
    if chosen_meme_id:
        chosen_meme_record = Meme.query.get(chosen_meme_id)
        chosen_meme_record.rating += 1
        db.session.commit()

    return render_template('index.html', memes=memes, img_sizes=img_sizes)

@app.route('/leaderboard')
def leaderboard():
    # get first 20 memes in order by rating
    top_20_memes = Meme.query.order_by(desc(Meme.rating)).limit(20).all()
    return render_template('leaderboard.html', memes=top_20_memes)