from django.test import TestCase
from mixer.backend.django import mixer

# Create your tests here.
class TestMashupAlgorithm(TestCase):
    def setUp(self):
        self.random_instance = mixer.blend('content.MashupAlgorithm', name='mouse_join')

    def tearDown(self):
        pass

    def test_mashup_algorithm_name(self):
        self.assertEquals(random_instance.name, 'mouse_join')
