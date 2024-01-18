#!/usr/bin/python3

'''BaseModel to be inherited'''

import uuid
from datetime import datetime
import models


class BaseModel:
    def __init__(self, *args, **kwargs):
        '''to create new or existing instance'''
        if kwargs is not None and kwargs != {}:
            timeformat = "%Y-%m-%dT%H:%M:%S.%f"
            for key in kwargs:

                if key == "created_at":
                    self.__dict__[key] = datetime.strptime(kwargs[key],
                                                           timeformat)
                elif key == "updated_at":
                    self.__dict__[key] = datetime.strptime(kwargs[key],
                                                           timeformat)
                else:
                    self.__dict__[key] = kwargs[key]
        
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        '''str repre'''
        return "[{}] ({}) {}".\
               format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        '''this edits the updated_at value to a new value of current time'''
        updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        '''returns a dict repre of an instance'''
        mydict = self.__dict__.copy()
        mydict["created_at"] = mydict["created_at"].isoformat()
        mydict["updated_at"] = mydict["updated_at"].isoformat()
        mydict["__class__"] = self.__class__.__name__

        return mydict
