from flask import Blueprint, request, render_template, redirect
from utils import Posts


bookmarks = Blueprint('bookmarks', __name__, template_folder='templates/bookmarks')

@bookmarks.route('/bookmarks')
def bookmarks_main_page():
    path = './static/data/bookmarks.json'
    posts_obj = Posts()
    bookmarks = posts_obj.json_uploader(path)
    return render_template('bookmarks.html', data=bookmarks)


@bookmarks.route('/bookmarks/add/<int:post_id>', methods=["GET"])
def add_page(post_id):
    posts_obj = Posts()
    post_by_id = posts_obj.get_post_by_pk(post_id)
    posts_obj.add_data_to_json(post_by_id)
    return redirect("/", code=302)


@bookmarks.route('/', methods=["POST"])
def add_by_button():
    post_id = request.form['bookmark_action']
    posts_obj = Posts()
    post_by_id = posts_obj.get_post_by_pk(post_id)
    posts_obj.add_data_to_json(post_by_id)
    return redirect("/", code=302)


@bookmarks.route('/bookmarks/remove/<int:post_id>', methods=['GET'])
def remove_page(post_id):
    posts_obj = Posts()
    post_by_id = posts_obj.get_post_by_pk(post_id)
    posts_obj.remove_data_from_json(post_by_id)
    return redirect("/", code=302)



