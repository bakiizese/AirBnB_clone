#!/usr/bin/python3

'''A python console to manipulate objects'''

import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import re
import ast


class HBNBCommand(cmd.Cmd):
    '''a cmd commad interpreter that loops to accept commands'''
    prompt = "(hbnb)"
    class_dict = {"BaseModel": BaseModel, "User": User,
                  "State": State, "City": City,
                  "Amenity": Amenity, "Place": Place, "Review": Review}

    def default(self, line):
        '''default method'''
        self.parse(line)

    def parse(self, line):
        '''to parse through line'''
        cl_name = re.search(r"(\w*)\.", line)
        cl_name = cl_name.group(1)
        func = re.search(r"\.(\w*)", line)
        func = func.group(1)
        if func == "all":
            self.do_all(cl_name)
        elif func == "count":
            self.do_count(cl_name)
        elif func == "show" or func == "destroy":
            ids = re.search(r"\(\"([\w-]*)\"\)", line)
            ids = ids.group(1)
            sh = cl_name + " " + ids
            if func == "show":
                self.do_show(sh)
            elif func == "destroy":
                self.do_destroy(sh)
        else:
            check = re.search("({.*})", line)
            if check:
                self.edit_update(line)
            else:
                c = re.search(r"(\w*)\.(\w*)\(\"([\w-]*)\"\,\s\"(\w*.*)\"\,\s",
                              line)
                c_cl = c.group(1)
                c_fun = c.group(2)
                c_id = c.group(3)
                c_at = c.group(4)
                val = re.search(r"(\"?\w+\"?)\)", line)
                val = val.group(1)
                if c_fun == "update":
                    cl = c_cl + " " + c_id + " " + c_at + " " + val
                    self.do_update(cl)

    def do_quit(self, line):
        '''Quit command to exit the program.'''
        return True

    def do_EOF(self, line):
        '''EOF command to end the program.'''
        print()
        return True

    def emptyline(self):
        '''to pass an emptyline with doing nothing'''
        pass

    def do_create(self, value):
        '''Creat command to create instance'''
        if value == "" or value is None:
            print("** class name missing **")
        elif value not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
        else:
            cl = HBNBCommand.class_dict[value]()
            cl.save()
            print(cl.id)

    def do_show(self, value):
        '''Show command to show a specific instance'''
        if value == "" or value is None:
            print("** class name missing **")
        else:
            cl = value.split(" ")
            if cl[0] not in HBNBCommand.class_dict:
                print("** class doesn't exist **")
            elif len(cl) < 2:
                print("** instance id missiing **")
            else:
                key = "{}.{}".format(cl[0], cl[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    d = storage.all()[key]
                    print(d)

    def do_destroy(self, value):
        '''Destroy to delete an instance'''
        if value == "" or value is None:
            print("** class name missinig **")
        else:
            cl = value.split(" ")
            if cl[0] not in HBNBCommand.class_dict:
                print("** class doesn't exist **")
            elif len(cl) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(cl[0], cl[1])
                if key not in storage.all():
                    print("** o instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, value):
        '''All command to print all'''
        if value == "" or value is None:
            ls = []
            for k, v in storage.all().items():
                ls.append(str(v))
            print(ls)
        elif value in HBNBCommand.class_dict:
            ls = []
            for k, v in storage.all().items():
                d = k.split(".")
                if d[0] == value:
                    ls.append(str(v))
            print(ls)
        else:
            print("** class doesn't exist **")

    def do_count(self, value):
        '''Count command to print number of instance'''
        count = 0
        if value == "" or value is None:
            for k in storage.all():
                count += 1
        else:
            for k, v in storage.all().items():
                d = k.split(".")
                if d[0] == value:
                    count += 1
        print(count)

    def edit_update(self, value):
        '''That edits a dict to pass to Update command'''
        rg = re.search(r"(\w*)\.(\w*)\(\"([\w-]*)\"\,\s({.*})", value)
        rg_cl = rg.group(1)
        rg_fun = rg.group(2)
        rg_id = rg.group(3)
        rg_dict = rg.group(4)
        my_dict = ast.literal_eval(rg_dict)
        for k, v in my_dict.items():
            if isinstance(v, int):
                v = str(v)
            st = rg_cl + " " + rg_id + " " + k + " " + v
            self.do_update(st)

    def do_update(self, value):
        '''Update command to update attribute of instance'''
        if value == "" or value is None:
            print("** class name missing **")
        else:
            cl = value.split(" ")
            if cl[0] not in HBNBCommand.class_dict:
                print("** class doesn't exist **")
            elif len(cl) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(cl[0], cl[1])
                if key not in storage.all():
                    print("** no instance found **")
                elif len(cl) < 3:
                    print("** attribute name missing **")
                elif len(cl) < 4:
                    print("** value missing **")
                else:
                    dic = storage.all()[key].__dict__
                    dic[cl[2]] = cl[3]
                    dic[cl[2]] = dic[cl[2]].strip('"')
                    storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
