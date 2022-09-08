from ast import Add
from flask_restful import Resource, abort, reqparse
from api import media


from .config import AddPath

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



path_perser = reqparse.RequestParser()
path_perser.add_argument('path', required=True, help='path')
path_perser.add_argument('name', required=True, help='path')
path_perser.add_argument('unstructure', required=True, help='path')
class AddFolder(Resource):
    def post(self):
        args = path_perser.parse_args()

        if AddPath(args['path'], args['name'], args['unstructure']):
            return {'message': 'added'}
        return {'message': 'could not be added'}, 400
