from flask import Flask, Blueprint, request, render_template, send_from_directory
from posts.posts import posts
from api.api import api
from tags.tags import tags
from bookmarks.bookmarks import bookmarks


app = Flask(__name__)

# Ограничиваем возможность загрузки бесконечных файлов
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

app.register_blueprint(posts)
app.register_blueprint(api)
app.register_blueprint(tags)
app.register_blueprint(bookmarks)


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


if __name__ == "__main__":
    app.run()


