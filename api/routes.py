from flask import send_from_directory
from api import app
from api import media


@app.route("/video/<string:file_id>")
def get_file(file_id):
    try:
        result = media.search_id(file_id)
        file_path = result['path']
        file = result["files"]
        return send_from_directory(file_path, file)
    except FileNotFoundError:
        return "", 404


@app.route("/image/<string:file_id>")
def get_image(file_id):
    try:
        try:
            result = media.search_id(file_id)
            file_path = result['path']
            file = result["thumbnail"]

            if file is None:
                return send_from_directory(app.root_path, 'static/images/logo.jpg')
        except FileNotFoundError:
            return send_from_directory(app.root_path, 'static/images/logo.jpg')
        return send_from_directory(file_path, file)
    except FileNotFoundError:
        return "", 404


@app.route("/reindex")
def reindex():
    media.reindex()
    return str(media.Media)
