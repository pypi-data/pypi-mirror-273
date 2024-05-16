import unittest
from html2object.html_element import HtmlElement


class TestHtmlElement(unittest.TestCase):

    def test_init(self):
        element = HtmlElement()
        self.assertEqual(element.name, "")
        self.assertEqual(element.id, "")
        self.assertEqual(element.attributes, {})
        self.assertEqual(element.children, [])

        element = HtmlElement(html="<div id='myDiv' class='container'></div>")
        self.assertEqual(element.name, "div")
        self.assertEqual(element.id, "'myDiv'")
        self.assertEqual(element.attributes, {"id": "'myDiv'", "class": "'container'"})
        self.assertEqual(element.children, [])

    def test_add_child(self):
        parent = HtmlElement(name="div")
        child = HtmlElement(name="span")
        parent.add_child(child)
        self.assertEqual(parent.children, [child])
        self.assertEqual(child.parent, parent)

    def test_set_children(self):
        parent = HtmlElement(name="div")
        children = [
            HtmlElement(name="span"),
            HtmlElement(name="p"),
            HtmlElement(name="a"),
        ]
        parent.set_children(children)
        self.assertEqual(parent.children, children)
        for child in children:
            self.assertEqual(child.parent, parent)

    def test_set_parent(self):
        parent = HtmlElement(name="div")
        child = HtmlElement(name="span")
        child.set_parent(parent)
        self.assertEqual(child.parent, parent)

    def test_find_element_by_id(self):
        parent = HtmlElement(name="div", id="parentDiv")
        child1 = HtmlElement(name="span", id="child1")
        child2 = HtmlElement(name="p", id="child2")
        child3 = HtmlElement(name="a", id="child3")
        parent.add_child(child1)
        parent.add_child(child2)
        child2.add_child(child3)

        result = parent.find_element_by_id("parentDiv")
        self.assertEqual(result, parent)

        result = parent.find_element_by_id("child1")
        self.assertEqual(result, child1)

        result = parent.find_element_by_id("child2")
        self.assertEqual(result, child2)

        result = parent.find_element_by_id("child3")
        self.assertEqual(result, child3)

        result = parent.find_element_by_id("nonexistent")
        self.assertIsNone(result)

    def test_find_element_by_id_with_real_html(self):
        parent = HtmlElement(open("tests/assets/index.html").read())

        result = parent.find_element_by_id("info-image")
        assert result.name == "img"
        assert result.id == "info-image"
        assert result.children is None
        assert result.parent.name == "div"

    def test_str(self):
        element = HtmlElement(name="div", id="myDiv", attributes={"class": "container"})
        self.assertEqual(str(element), "<div id=myDiv class=container/>")

        element = HtmlElement(name="div")
        element.add_child("Hello, World!")
        self.assertEqual(str(element), "<div>Hello, World!</div>")


if __name__ == "__main__":
    unittest.main()
