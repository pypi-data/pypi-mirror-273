from unittest import TestCase

from geneeanlpclient.g3.model import GkbProperty


class TestModel(TestCase):

    def test_gkbproperty(self):
        with self.assertRaises(ValueError):
            prop = GkbProperty(name='test', label='test')

    def test_gkbproperty_equals(self):
        gkbProp1 = GkbProperty(name='description', label='popis', strValue='německá politička')
        gkbProp2 = GkbProperty(name='description', label='popis', strValue='německá politička')
        self.assertNotEquals('foo', gkbProp1)
        self.assertEqual(gkbProp1, gkbProp2)
