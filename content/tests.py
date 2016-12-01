from django.test import TestCase
from mixer.backend.django import mixer

# Create your tests here.
class TestMashupAlgorithm(TestCase):
    def setUp(self):
        self.random_instance = mixer.blend('content.MashupAlgorithm', name='mouse_join')

    def tearDown(self):
        pass

    def test_mashup_algorithm_name(self):
        foo = str(self.random_instance)
        self.assertEquals(str(self.random_instance), 'mouse_join', 'str should return self.name')

    def test_mashup_algorithm_repr_isset(self):
        foo = self.random_instance
        self.assertEquals(repr(self.random_instance), 'mouse_join', 'repr should be equal to self.name')

    def test_mashup_algorithm_usage_count_is_not_null(self):
        self.assertIsNotNone(self.random_instance.usage_count)


