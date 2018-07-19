from django.test import TestCase

# Create your tests here.


from django.test import TestCase
import datetime
from django.utils import timezone

from enron.models import Email,ToEmail,CcEmail,BccEmail
from scripts import inemaila

from scripts.inemaila import EnronEmail






from django.test import TestCase

class AnimalTestCase(TestCase):
    #def setUp(self):
        #Animal.objects.create(name="lion", sound="roar")
        #Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        #lion = Animal.objects.get(name="lion")
        #cat = Animal.objects.get(name="cat")
        #self.assertEqual(lion.speak(), 'The lion says "roar"')
        #self.assertEqual(cat.speak(), 'The cat says "meow"')
        mailpath = "/home/freddie/PycharmProjects/testdata/"
        inemaila.importData(mailpath)

class ClearAllData(TestCase):
    BccEmail.objects.d


