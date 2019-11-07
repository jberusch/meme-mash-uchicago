from bs4 import BeautifulSoup
from app import db
from app.models import Meme

with open('scraping_resources/from_fb_group.html', 'rb') as fp:
    soup = BeautifulSoup(fp, 'lxml')
    divs = soup.find_all('div', rel='gallery')

    count = 0
    for div in divs:
        count += 1
        # set vars
        filename = ''
        caption = ''
        for child in div.children:
            # test if link to photo
            href = child.get('href')
            if href:
                filename = href.split('/')[-1]
            
            # test if div with caption
            class_name = child.get('class')
            if class_name[0] == 'caption':
                if child.p and len(child.p.contents) > 0:
                    cap = str(child.p.contents[0])
                    caption = '' if '</' in cap else cap
        
        print('Meme:\nFilename: {}\nCaption: {}\n\n'.format(filename, caption))

        # add entry to DB
        new_meme = Meme(filename=filename, caption=caption, rating=0.0, num_contests=0, num_no_meme_votes=0)
        db.session.add(new_meme)
    
    print('Memes counted: {}'.format(count))
    db.session.commit()