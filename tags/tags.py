from flask import Blueprint, request, render_template
from utils import Posts

tags = Blueprint('tags', __name__, template_folder='templates/tags')


@tags.route('/tag/<tag_name>')
def tags_page(tag_name):
    post_obj = Posts()
    match_list = post_obj.posts_search_by_hashtag(tag_name)
    tag_name = tag_name.replace('{','').replace("}","").upper()
    return render_template('tag.html', data=match_list, tag=tag_name)
