from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm,UpdateProfile,BlogForm,CommentForm,SubscriptionForm
from ..models import User,BlogPost,Comment
from flask_login import login_required,current_user
from .. import db
from ..request import get_quote

@main.route('/')
def index():
    
    '''
    View root page function that returns the index page and its data
    '''
    quote = get_quote()
    blog=BlogPost.query.all()
  
    title = 'Home'
    return render_template('index.html', title = title,blog=blog,quote=quote)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
@main.route('/pitch/new', methods=['GET','POST'])
@login_required
def create_blogs():
    form = BlogForm()
    if form.validate_on_submit():
        title=form.title.data
        blog_post=form.blog_post.data
        new_blog = BlogPost(name=name,blog_post=blog_post, user=current_user)
        new_blog.save_blog()

        return redirect(url_for('main.index'))

    return render_template('blog.html',form = form)   

@main.route('/comment/new/<int:id>', methods=['GET','POST'])
@login_required
def add_comments(id):
    form = CommentForm()
    if form.validate_on_submit():
        name=form.name.data
        comment=form.comment.data
        new_comment = Comment(comment=comment,blogposts_id=id, user=current_user)
        
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('main.index'))
    comment=Comment.query.filter_by(blogposts_id=id).all()


    return render_template('comment.html',comment=comment,form =form)   

