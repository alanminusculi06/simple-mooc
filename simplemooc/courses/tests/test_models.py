from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.urls import reverse
from django.conf import settings
from model_mommy import mommy

from simplemooc.courses.models import Course

class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.coursesDjango = mommy.make('courses.Course', name='Python na web com Django', _quantity=5)
        self.coursesDev = mommy.make('courses.Course', name='Python para Devs', _quantity=10)
        self.client = Client()

    def tearDown(self):
        Course.objects.all().delete()

    def test_course_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search = Course.objects.search('dev')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('python')
        self.assertEqual(len(search), 15)


    
