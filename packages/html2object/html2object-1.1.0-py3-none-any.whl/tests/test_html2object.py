import unittest
from html2object.html2object import *


class TestHtml2Object(unittest.TestCase):

    def test_get_element(self):
        html = "<div class='container'><h1>Title</h1></div>"
        element = get_element(html, name="h1")
        self.assertEqual(element, "<h1>")

    def test_remove_element(self):
        html = "<div class='container'><h1>Title</h1></div>"
        new_html = remove_element(html, name="h1")
        self.assertEqual(new_html, "<div class='container'></div>")

    def test_get_name(self):
        html = "<div class='container'><h1>Title</h1></div>"
        name = get_name(html)
        self.assertEqual(name, "div")

    def test_get_attributes(self):
        html = "<div id='main' class='container'><h1>Title</h1></div>"
        attributes = get_attributes(html)
        expected_attributes = {"id": "'main'", "class": "'container'"}
        self.assertEqual(attributes, expected_attributes)

    def test_get_child(self):
        html = "<div><span>Child</span></div>"
        child = get_child(html, name="div")
        self.assertEqual(child, "<span>Child</span>")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
