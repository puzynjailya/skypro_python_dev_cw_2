from flask import Blueprint, jsonify
from utils import Posts

api = Blueprint('api', __name__)


@api.route('/api/posts')
def api_all_posts():
    posts = Posts()
    all_posts = posts.json_uploader()
    return jsonify(all_posts)


@api.route('/api/posts/<int:post_id>')
def single_post(post_id):
    posts = Posts()
    single_post = posts.get_post_by_pk(post_id)
    return jsonify(single_post)