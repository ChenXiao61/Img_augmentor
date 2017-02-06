from unittest import TestCase, main
from tempfile import TemporaryDirectory
import Augmentor


class ImageSourceTestCase(TestCase):
    def setUp(self):
        self.test_dir = TemporaryDirectory()


class TestAugmentor(TestCase):

    def setUp(self):
        self.hello_message = "Hello."

if __name__ == 'main':
    main()
