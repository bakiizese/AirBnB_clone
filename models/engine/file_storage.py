#!/usr/bin/python3
'''to save and reload instance to file'''
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    '''store file and retrive file'''
    __file_path = 'file.json'
    __objects = {}
    classes = {"BaseModel": BaseModel, "User": User,
               "State": State, "City": City,
               "Amenity": Amenity, "Place": Place, "Review": Review}

    def all(self):
        '''returns __objects'''
        return FileStorage.__objects

    def new(self, obj):
        '''creates key to hold name.id'''
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        '''saves to file'''
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            dic = {}
            for key, v in FileStorage.__objects.items():
                dic[key] = v.to_dict()
            json.dump(dic, f)

    def reload(self):
        '''reloads file'''
        if not os.path.exists(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
            new_obj_dict = json.load(f)
            for key, value in new_obj_dict.items():
                obj = FileStorage.classes[value['__class__']](**value)
                self.__objects[key] = obj
