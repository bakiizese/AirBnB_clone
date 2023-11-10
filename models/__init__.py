#!/usr/bin/python3
'''to reload automaticaly and create storage var of file storage'''
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
