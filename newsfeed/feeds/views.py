from flask import render_template, flash, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required
from newsfeed import db
from newsfeed.models import News
from newsfeed.feeds.forms import NewsFeedForm


news_feed_b = Blueprint('news_feed', __name__)

#Creating blog post
@news_feed_b.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form = NewsFeedForm()

    if form.validate_on_submit():

        news_feed = News(title=form.title.data, text=form.text.data, user_id=current_user.id)

        db.session.add(news_feed)
        db.session.commit()

        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


#updating blog post

@news_feed_b.route("/<int:news_feed_id>/update", methods=['GET','POST'])
@login_required
def update(news_feed_id):
    news_feed = News.query.get_or_404(news_feed_id)

    if news_feed.author != current_user:
        return redirect(url_for('error_pages.error_403'))

    form = NewsFeedForm()

    if form.validate_on_submit():
        news_feed.title = form.title.data
        news_feed.text = form.text.data
        db.session.commit()

        return redirect(url_for('news_feed.news_feed',news_feed_id = news_feed_id))

    elif request.method == 'GET':
        form.title.data = news_feed.title
        form.text.data = news_feed.text

    return render_template('create_post.html',title='Updating', form=form)



#deleting blog post
@news_feed_b.route('/<int:news_feed_id>/delete', methods=['GET','POST'])
@login_required
def delete_post(news_feed_id):
    news_feed = News.query.get_or_404(news_feed_id)

    if news_feed.author != current_user:
        return redirect(url_for('error_pages.error_403'))

    db.session.delete(news_feed)
    db.commit()
    flash("Blog post deleted")
    return redirect(url_for('core.index'))


#viewing blog post
@news_feed_b.route('/<int:news_feed_id>')
def news_feed(news_feed_id):
    news_feed = News.query.get_or_404(news_feed_id)
    return render_template('news_feed.html', title=news_feed.title, date=news_feed.date, post=news_feed)
