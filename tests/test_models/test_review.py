#!/usr/bin/python3
''' tests the basemodel file '''
import os
import models
import unittest
from models.review import Review
from time import sleep
from datetime import datetime


class Test_review(unittest.TestCase):
    '''tests the Base class'''
    def test_instance_type(self):
        self.assertEqual(Review, type(Review()))

    def test_id_is_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_and_updated_at_type(self):
        self.assertEqual(datetime, type(Review().created_at))
        self.assertEqual(datetime, type(Review().updated_at))

    def test_two_instace_are_not_equal(self):
        in1 = Review()
        in2 = Review()
        self.assertNotEqual(in1.id, in2.id)

    def test_time_difference_created_at(self):
        in1 = Review()
        sleep(0.05)
        in2 = Review()
        self.assertLess(in1.created_at, in2.created_at)

    def test_time_diference_updated_at(self):
        in1 = Review()
        sleep(0.05)
        in2 = Review()
        self.assertLess(in1.updated_at, in2.updated_at)

    def test_created_with_kwargs(self):
        tm = datetime.today()
        tms = tm.isoformat()
        in1 = Review(id="1111", created_at=tms, updated_at=tms)
        self.assertEqual(in1.id, "1111")
        self.assertEqual(in1.created_at, tm)
        self.assertEqual(in1.updated_at, tm)


class Test_BaseModel_save(unittest.TestCase):
    '''tests save method'''
    @classmethod
    def setUP(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass

    def test_save(self):
        in1 = Review()
        update = in1.updated_at
        sleep(0.10)
        in1.save()
        self.assertEqual(update, in1.updated_at)


class Test_to_dict(unittest.TestCase):
    '''tests to_dict method'''
    def test_what_it_conatains(self):
        in1 = Review()
        self.assertIn("id", in1.to_dict())
        self.assertIn("__class__", in1.to_dict())
        self.assertIn("created_at", in1.to_dict())
        self.assertIn("updated_at", in1.to_dict())

    def test_type(self):
        in1 = Review()
        self.assertTrue(dict, type(in1.to_dict()))

    def test_attributes(self):
        in1 = Review()
        in1.name = "ALX"
        in1.num = 12
        self.assertIn("name", in1.to_dict())
        self.assertIn("num", in1.to_dict())


if __name__ == "__main__":
    unittest.main()
