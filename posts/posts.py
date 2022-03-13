from flask import Blueprint, request, render_template
import logging
from utils import Posts
from exceptions import *

posts = Blueprint('posts', __name__, template_folder='templates/posts')

# Задаем лимит количества выводимых постов при поиске
posts_limit = 10


@posts.route('/')
def index_page():
    try:
        posts_obj = Posts()
        all_posts = posts_obj.json_uploader()
        all_posts = posts_obj.update_hashtags()
        decoded_bookmarks_json = posts_obj.json_uploader('./static/data/bookmarks.json')
        bookmarks_number = len(decoded_bookmarks_json)
        return render_template('index.html', all_posts=all_posts, bookmarks_number=bookmarks_number)
    except DataLoaderError:
        return render_template('data_load_error.html')


@posts.route('/post/<int:pk>')
def post_page(pk):
    try:
        posts_obj = Posts()
        post_by_id = posts_obj.get_post_by_pk(pk)
        comments_by_id = posts_obj.get_comments_by_post_id(pk)
        if len(comments_by_id) == 0:
            comments_by_id = ''
        return render_template('post.html', post_data=post_by_id, comments=comments_by_id)
    except TypeError:
        return 'У-у-у-у-х, что-то не то с ИД поста'
    except PostIDCountError:
        return 'У-у-у-у-х, что-то пошло не так с количество ИД постов'
    except IDDoesntExistError:
        return 'У-у-у-у-х, поста с таким ID не существует :_('


@posts.route('/search/', methods=['GET'])
def search_page():
    is_notfound = False
    posts_obj = Posts()
    target = request.args.get('sv', "")
    match_list = posts_obj.posts_search(target)
    if len(match_list) == 0:
        is_notfound = True
    return render_template('search.html', match_list=match_list, is_notfound=is_notfound, target=target)


@posts.route('/search/', methods=['POST'])
def search_request():
    search_word = request.form['sv']
    posts_obj = Posts()
    match_list = posts_obj.posts_search(search_word)
    # Если список пустой, то выводим информацию, что постов не найдено
    if len(match_list) == 0:
        is_notfound = True
    # Если список содержит более лимита значений, то выводим только первые значения по лимиту
    if len(match_list) >= posts_limit:
        match_list = match_list[:posts_limit]

    return render_template('search.html', match_list=match_list, is_notfound=is_notfound, target=search_word)

@posts.route('/users/<user_name>')
def users_page(user_name):
    is_notfound = False
    posts_obj = Posts()
    user_feed = posts_obj.get_posts_by_user(user_name)
    if len(user_feed) == 0:
        is_notfound = True
    if len(user_feed) >= posts_limit:
        user_feed = user_feed[:posts_limit]

    return render_template('user-feed.html', user_feed=user_feed, is_notfound=is_notfound, user_name=user_name)

