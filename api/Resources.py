from flask_restful import Resource, abort
from api import media


def about_if_file_not_found():
    abort(404, message="Video not Found")


class Videos(Resource):
    def get(self):
        return media.Media


class GetData(Resource):
    def get(self, section):
        try:
            data = media.Media[section]
            return data
        except KeyError:
            return "section dose not exist"


class MetaData(Resource):
    def get(self):
        metadata = []
        for d in media.Media:
            length = len(media.Media[d])
            meta = {
                d: length
            }
            metadata.append(meta)
        return metadata


class Search(Resource):
    def get(self, term):
        try:
            result = media.search(term)
            return result
        except FileNotFoundError:
            abort(404, message="Video not Found")


class SearchId(Resource):
    def get(self, search_id):
        result = media.search_id(search_id)
        return result
