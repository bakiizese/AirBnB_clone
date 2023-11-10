#!/usr/bin/python3
'''user class'''
from models.base_model import BaseModel


class User(BaseModel):
    '''creats user'''
    email = ""
    password = ""
    first_name = ""
    last_name = ""
