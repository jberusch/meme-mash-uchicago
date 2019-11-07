# local imports
from app import app, db
from app.models import Meme

# library imports
from PIL import Image
from io import BytesIO
from sqlalchemy import desc
from random import randrange
from flask import render_template, request

# r1 = expected result for chosen
# r2 = expected result for other
def get_expected_scores(r1=0, r2=0):
    p1 = (1.0 / (1.0 + pow(10, ((r1 - r2) / 400))))
    p2 = (1.0 / (1.0 + pow(10, ((r2 - r1) / 400))))

    print(p1, p2)
    return (p1, p2)

@app.route('/')
@app.route('/index')
def index():
    # get meme db entry
    all_memes = Meme.query.all()

    # TODO: make this its own function
    # sample 2 random memes
    num_memes = len(all_memes)
    meme1_index = randrange(num_memes - 1)
    meme2_index = randrange(num_memes - 1)

    # make sure memes are different
    while meme2_index == meme1_index:
        meme2_index = randrange(num_memes - 1)
    memes = []
    memes.append(all_memes[meme1_index])
    memes.append(all_memes[meme2_index])

    # get meme image sizes
    # TODO: make this its own function
    img_sizes = []
    for meme in memes:
        with open('app/static/memes/{}'.format(meme.filename), 'rb') as fp:
            img_bytes = BytesIO(fp.read())
            img = Image.open(img_bytes)
            size = img.size
            ratio = size[0] / size[1]

            # TODO: adjust these sizes later by ratio

            adjusted_size = (800, 600)
            img_sizes.append(adjusted_size)
            
    # get selection
    chosen_meme_id = request.args.get('choice')
    other_meme_id = request.args.get('other')
    
    # TODO: make this its own function
    # if user made a choice, update the scores
    if chosen_meme_id:
        # define scaling constant
        k = 25

        chosen_meme_record = Meme.query.get(chosen_meme_id)
        other_meme_record = Meme.query.get(other_meme_id)

        # get expected scores from the chosen and the other
        expected_scores = get_expected_scores(chosen_meme_record.rating, other_meme_record.rating)

        # update scores of both, given chosen as victor
        new_chosen_score = chosen_meme_record.rating + k * (1 - expected_scores[0])
        new_other_score = other_meme_record.rating + k * (0 - expected_scores[1])
        chosen_meme_record.rating = new_chosen_score
        other_meme_record.rating = new_other_score

        chosen_meme_record.num_contests += 1
        other_meme_record.num_contests += 1
    
        # update DB
        db.session.commit()

    return render_template('index.html', memes=memes, img_sizes=img_sizes)

@app.route('/leaderboard')
def leaderboard():
    # get first 20 memes in order by rating
    top_20_memes = Meme.query.order_by(desc(Meme.rating)).limit(20).all()
    return render_template('leaderboard.html', memes=top_20_memes)