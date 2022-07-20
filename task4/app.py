"""
    - API to create URL with random short name (something like this url/78sda8s6d),
        url random name should be fixed size string and unique per url
    - API for premium clients to create URL with custom name (url/&lt;custom&gt;)
    - Input url validation, that it is a correct url and size must be below 250 characterAu
    - Counters - how many times the url was accessed (optional requirement)
    - Automatic deletion of urls older than 30 days (optional requirement)
"""


from flask import render_template, request, flash, redirect, url_for, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os 
from datetime import datetime, timedelta
 


basedir = os.path.abspath(os.path.dirname(__file__))

#აპის კონფიგურაცია 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shorty.db') #ბასა კეთდება ამ მისამართზე 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#იქნება მოდელები
class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(250), nullable=False)
    short_id = db.Column(db.String(8), nullable=False, unique=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    access_counter = db.Column(db.Integer, default = 0)
    # premium_acc = db.Column(db.Boolean, default = False)
    # created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    #კოონსტრუქტორი
    def __init__(self, original_url, short_id, time, access_counter):
        self.original_url  = original_url
        self.short_id = short_id
        self.time = time
        self.access_counter = access_counter

    #ვადაგასულების წასაშლელი მეთოდი გაეშვება ვეგ-გვერის ოველი ახალი ჩატვირთვისას 
    @classmethod
    def delete_expired(self):
        limit = datetime.utcnow() - timedelta(30)
        for url in ShortUrls.query.order_by(ShortUrls.id).all():
            if limit > url.time:
                db.session.delete(url)
        db.session.commit()

# db.drop_all()
# db.create_all()

# st1 = ShortUrls("name", "sname", datetime.utcnow(), 2)
# st3 = ShortUrls("zura", "begadze", datetime.now() - timedelta(days=100), 0)

# db.session.add_all([st3, st1])

# db.session.commit()


from random import choice
import string

# შორტების გენერატორიი 
def generate_short_id(num_of_chars: int):
    
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


#აქ იტვირთება ინდეხს გვერდი
@app.route('/', methods=['GET', 'POST'])
def index():    
    ShortUrls.delete_expired() #წაშლა ელემენტების ვადაგასულეის]]

    if request.method == 'POST':
        url = request.form['url']
        short_id = request.form['custom_id']

        if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
            flash('Please enter different custom id!')
            return redirect(url_for('index'))

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        if not short_id:
            short_id = generate_short_id(6)

        #ინახებ ბაზაში 

        new_link = ShortUrls(url, short_id, datetime.utcnow(), 0)
        db.session.add(new_link)
        db.session.commit()
        short = ShortUrls.query.order_by(-ShortUrls.id).all()
        short_url = request.host_url + short_id

        return render_template('index.html', short_url=short_url, short= short)

    return render_template('index.html')

#შორტებზე დაგასასვლელი ფუქნცი ა
@app.route('/<short_id>')
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    #ბაზაში ზრდის წვდომების რაოდენობას ამ ლინკზე
#     if link.access_counter:
    link.access_counter+=1
    db.session.commit()

    if link:
        return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
