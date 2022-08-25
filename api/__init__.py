from flask import Flask
from flask_restful import Api
from api.config import Download_path
app = Flask(__name__)
api = Api(app)


from api.MediaLib import MediaLib


media = MediaLib()

media.add_media(Download_path, "download", unstructured=True)
media.add_media("/home/ivan/Videos", "videos",unstructured=True)




from api.Resources import Videos, GetData, MetaData, Search, SearchId
from api import routes
from api import api_errors

api.add_resource(Videos, "/")
api.add_resource(GetData, "/<section>")
api.add_resource(MetaData, "/metadata")
api.add_resource(Search, "/search/<string:term>")
api.add_resource(SearchId, "/search_id/<string:search_id>")
