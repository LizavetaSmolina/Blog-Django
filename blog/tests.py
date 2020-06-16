from django.test import TestCase
from .models import Post, Blog

class PostModelTests(TestCase):

    def test_title_max_length(self):
        post=Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length,100)

    def test_description_max_length(self):
        post=Post.objects.get(id=1)
        max_length = post._meta.get_field('description').max_length
        self.assertEquals(max_length,300)

class BlogModelTests(TestCase):

    def test_title_max_length(self):
        blog=Blog.objects.get(id=1)
        max_length = blog._meta.get_field('title').max_length
        self.assertEquals(max_length,100)

    def test_category_max_length(self):
        blog=Blog.objects.get(id=1)
        max_length = blog._meta.get_field('category').max_length
        self.assertEquals(max_length,100)

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
# Create your tests here.
