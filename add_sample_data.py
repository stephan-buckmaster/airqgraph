import csv
from app import app
from app import db            
from api.models import Post
count = 0
with app.app_context():
    db.session.query(Post).delete()
    with open('data/posts.csv', encoding='utf-8', newline='') as csv_file:
        csvreader = csv.DictReader(csv_file, quotechar='"')
        for row in csvreader:
            count += 1
            post = Post(**row)
            post.created_at = db.func.now()
            db.session.add(post)

    db.session.commit()

print(f'Database has {count} post records')
