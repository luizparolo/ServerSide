# Main program, with main functions and rendering routines
# --------------------

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from datetime import datetime
from app import app, db, lm, oid
from .forms import LoginForm, EditForm
from .models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


# -- / equals /index html template --
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'Pele'},
            'body': 'Today the world is becoming better with the cure of ignorance!'
        },
        {
            'author': {'nickname': 'Uncle Sam'},
            'body': 'What do you thing abot to fly over New York without wings ?'
        },
               {
            'author': {'nickname': 'Hamilton'},
            'body': 'As soon as possible we will save money in order to buy a brande new house.'
        },
        {
            'author': {'nickname': 'Paris Hilton'},
            'body': 'Hey Andre, I have some free tickets for the suite of Hilton Vancouver.'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

# -- /login template --
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler

# -- Login Fuction --
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


# -- Logout routine --
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# -- User/<login> --
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Underrate bands with cool songs, please check my blog'},
        {'author': user, 'body': 'Tonight free food in the Marketplace at Waterfront Station'},
        {'author': user, 'body': '... ops, there will be also free pop and lemonade.'},
        {'author': user, 'body': 'Forecast for the week: lots of sun and highest of 24C.'},
        {'author': user, 'body': 'Probably with some rain only next Saturday, between 1 and 4 AM.'},
        {'author': user, 'body': 'Thats all folks !'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)

# -- Edit template --
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


# -- Error handler for 'Page Not Found' --
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# -- Error handler for 'Internal Error' --
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500