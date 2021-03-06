from flask import Flask, request, render_template, redirect, url_for
from data.db_interface import engine, Tweet
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime, timedelta
from data.settings import MAX_POPULAR_TWEETS, MAX_RECENT_TWEETS

app = Flask(__name__.split('.')[0])
#app.config.from_object(__name__)

@app.route('/')
def index():
    return redirect(url_for('recent_tweets'))

@app.route('/popular_tweets/')
def popular_tweets():
    Session = sessionmaker(bind=engine)
    s = Session()

    hashtag = "#SaveTheInternet" #the hashtag that we will trend today.
    
    popular_tweets = s.query('tweet','user','tweet_id','tweeted_on'). \
                          from_statement(text(
                            "select distinct on (tweets.user) * from tweets where tweet_type = 'popular' \
                             order by tweets.user, weight desc, tweeted_on desc limit %s" % MAX_POPULAR_TWEETS )).all()

    return render_template('tweets.html', tweets = popular_tweets, type_of_tweets = 'popular')

@app.route('/recent_tweets/')
def recent_tweets():
    Session = sessionmaker(bind=engine)
    s = Session()

    hashtag = "#SaveTheInternet" #the hashtag that we will trend today.
    
    #we will display collected tweets in last 12 hours
    last_12_hours = datetime.now() - timedelta(hours=12);

    recent_tweets = s.query('tweet','user','tweet_id','tweeted_on'). \
                          from_statement(text(
                            "select distinct on (tweets.user) * from tweets where tweet_type = 'recent' \
                             and tweeted_on >= (now() - interval '12 hours') \
                             and tweet not like 'RT%%' \
                             order by tweets.user, tweeted_on desc, weight desc limit %s" % MAX_RECENT_TWEETS)).all()

    return render_template('tweets.html', tweets = recent_tweets, type_of_tweets = 'recent')

#@app.route('/submitted_tweets/')
#def submitted_tweets():
#    return render_template('base.html', message = "No tweets here yet! Please submit some by tweeting us at http://twitter.com/_yalgaar/ :)")
