from pickle import FALSE
from . import media
from . import app
import json


# config filepath that you want to add
# example

config = {}
try:
    with open( app.root_path + '/bin/config.json', 'r') as f:
        config = json.load(f)
except:
    config = {
        "paths":
        [
            
        ]
    }
    with open( app.root_path + '/bin/config.json', 'w') as f:
        json.dump(config, f)

for path in config['paths']:
    media.add_media(path['path'],path['name'], path['unstructured'])



def AddPath(path, name, unstructured=True):
    config['paths'].append(
        {'path':path,'name':name, 'unstructured':unstructured}
    )
    media.add_media(path, name,unstructured)
    print(path, unstructured)
    try:
        with open( app.root_path + '/bin/config.json', 'w') as f:
            json.dump(config, f)
        media.reindex
        return True 
    
    except:
        return False
    


    

