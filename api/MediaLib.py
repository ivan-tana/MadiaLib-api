import json
import os
import uuid


def index_unstructured_folder(path: str, file_types: list):
    """
    if folder files do not have a structure
    :param path:  path were the file's reside
    :param file_types:  a list of file extensions for files that are to be added in the files list
    :return: returns a dictionary with keys id , path , name , files
        id: unique identifier for each file's
        path: path to the file's
        name: name of the folder
        structured: False
        files: a list if the files with  a file extension in the file_extension variable
        file_names names of the files in the folder
    """

    files = []
    for [path, _, folder_files] in os.walk(path):
        file_names = []
        matched_files = []
        if not len(folder_files) == 0:
            for file in folder_files:
                try:
                    
                    if file.rsplit(".", 1)[1] in file_types:
                       
                        matched_files.append(file)
                        file_names.append(file.rsplit(".", 1)[0])
                except:
                    pass

                if type(matched_files) == list and len(matched_files) > 1:
                    matched_files.sort()
                
                
            for file in matched_files:
               
                file_data = {
                    "id": str(uuid.uuid4()),
                    "path": path,
                    "name": str(file).rsplit(".", 1)[0],
                    "files": file,
                    "structured": False,
                    "thumbnail": None
                }
                files.append(file_data)

    if len(files) == 0:
        pass
    else:
        return files


def index_structured_folder(path: str, file_types: list):
    """
    if folder has been structured in the form
        path:
        ----folder:
        -------files
    :param path: the path were your structured files reside
    :param file_types: a list of file extensions for files that are to be added in the files list
    :return: returns a dictionary with keys id , path , name , files
        id: unique identifier for each file's
        path: path to the file's
        name: name of the folder
        structured: True
        files: a list if the files with  a file extension in the file_extension variable

    """
    files = []
    for [path, _, folder_files] in os.walk(path):
        match_files = []

        if not len(folder_files) == 0:
            for file in folder_files:
                thumbnail = "thumbnail.png"
                if file.rsplit(".", 1)[1] in file_types:
                    match_files.append(file)
                if file.rsplit(".", 1)[-1] in ['png', 'jpg', 'jpeg']:
                    thumbnail = file
            if not len(match_files) == 0:
                if len(match_files) == 1:
                    match_files = match_files[0]
                if type(match_files) == list and len(match_files) > 1:
                    match_files.sort()

                file_data = {
                    "id": str(uuid.uuid4()),
                    "path": path,
                    "name": str(path).rsplit("\\", 1)[-1],
                    "files": match_files,
                    "structured": True,
                    "thumbnail": thumbnail
                }
                files.append(file_data)
    if len(files) == 0:
        pass
    else:
        return files


def create_index(name: str, data, index_path=''):
    if file_exist(index_path, name + '.json'):
        if name == "index":
            with open(index_path + 'index.json', 'w') as f:
                json.dump(data, f, indent=2)
        return
    if not file_exist(index_path, name + '.json') or name == "index":
        with open(index_path + name + '.json', 'w') as f:
            json.dump(data, f, indent=2)


def file_exist(path, name):
    try:
        open(path + name)
        return True
    except FileNotFoundError:
        return False


def create_folder(path: str, name: str):
    try:
        if "/" in name:
            os.mkdir(path + name + "/")
        else:
            os.mkdir(path + name)
        return True
    except FileExistsError:
        return False


class MediaLib:
    def __init__(self):
        self.Media = {}
        self.index = []
        self.index_path = "index/"
        self._reindex_data = {}
        self.video_extensions = ['mp4', 'avi', 'mkv','webm']

    @property
    def index_path(self):
        self._change_index_path(self._index_path)
        return self._index_path

    @index_path.setter
    def index_path(self, value):
        self._change_index_path(value)
        self._index_path = value

    @property
    def video_extensions(self):
        return self._video_extensions

    @video_extensions.setter
    def video_extensions(self, value):
        self.reindex()
        if type(value) == str:
            value = [value]
        self._video_extensions = value

    def add_media(self, path: str, name: str, unstructured=False):
        """
        add a media folder and data to the media class
        :param unstructured: if the folder has a structure
            example:
                folder:
                ----media folder with media name:
                --------media files
                ----media folder with media name:
                --------media files
        :param path: folder path to the folder
        :type name: name of the media to be created
        """
        self._reindex_data[name] = {
            "path": path,
            "unstructured": unstructured
        }
        if not unstructured:
            media_data = index_structured_folder(path, self.video_extensions)
        else:
            media_data = index_unstructured_folder(path, self.video_extensions)
        if not file_exist(self.index_path, name + '.json'):
            self.Media[name] = media_data
        else:
            self.Media[name] = self._load_index(name)
        create_index(name, media_data, self.index_path)
        create_index("index", self.Media, self.index_path)

    def __call__(self):
        return self.Media

    def __repr__(self):
        return self.Media

    def __len__(self):
        return len(self.Media)

    def _load_index(self, name: str):
        with open(self.index_path + name + '.json') as f:
            return json.load(f)

    def search(self, term, search_all=True, media_name='index'):
        match_data = []
        if search_all:
            data = self._load_index('index')
            for m in data:
                for item in data[m]:
                    name = str(item['name']).lower()
                    term = term.lower()
                    if term in name or name.startswith(term) or name.endswith(term):
                        match_data.append(item)
        else:
            data = self._load_index(media_name)
            for item in data:
                name = str(item['name']).lower()
                term = term.lower()
                if term in name or name.startswith(term) or name.endswith(term):
                    match_data.append(item)

        if not match_data:
            raise FileNotFoundError
        else:
            return match_data

    def search_id(self, file_id: str, search_all=True, media_name=''):
        if search_all:
            data = self._load_index('index')
            for m in data:
                for item in data[m]:
                    if str(item['id']) == file_id:
                        return item
            raise FileNotFoundError
        else:
            data = self._load_index(media_name)
            if type(data) == dict:
                return ''
            else:
                for item in data:
                    if item['id'] == file_id:
                        return item

    def reindex(self):
        for name in self.Media:
            with open(self.index_path + name + '.json', 'w') as f:
                if self._reindex_data[name]['unstructured']:
                    media_data = index_unstructured_folder(self._reindex_data[name]["path"], self.video_extensions)
                    json.dump(media_data, f, indent=2)
                else:
                    media_data = index_structured_folder(self._reindex_data[name]["path"], self.video_extensions)
                    json.dump(media_data, f, indent=2)

                self.Media[name] = media_data
            with open(self.index_path + 'index.json', 'w') as f:
                json.dump(self.Media, f, indent=2)

    def _change_index_path(self, path):
        create_folder("", path)
