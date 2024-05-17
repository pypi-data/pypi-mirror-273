import uuid
import json
import html2object as html_u


class HtmlElement:
    def __init__(
        self,
        html: str = "",
        id: str = "",
        name: str = "",
        attributes: dict = {},
        parent: object | None = None,
        children: list = [],
    ):
        self.uuid = str(uuid.uuid4())
        self.parent = parent
        if html:
            self._parse(html)
            return
        self.id = id
        self.name = name
        self.attributes = {"id": id, **attributes} if id else attributes
        self.children = children

    def add_child(self, child: str | object) -> object:
        if not self.children:
            self.children = []
        if type(child) == HtmlElement:
            child.set_parent(self)
        self.children.append(child)
        return self

    def set_children(self, children: list) -> object:
        self.children = []
        for child in children:
            if type(child) == HtmlElement:
                child.set_parent(self)
            self.children.append(child)
        return self

    def set_parent(self, parent: object) -> object:
        self.parent = parent
        return self

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def get_attribute(self, key):
        return self.attributes.get(key)

    def get_element_by_id(self, id: str, pile: list = None) -> object | None:
        if pile is None:
            pile = []
        if self.id == id:
            return self
        if self.uuid in pile:
            return None
        pile.append(self.uuid)

        result = self.parent.get_element_by_id(id, pile) if self.parent else None
        if self.children and not result:
            for child in self.children:
                result = (
                    None if type(child) == str else child.get_element_by_id(id, pile)
                )
                if result:
                    break
        return result

    def get_elements_by_name(self, name: str) -> list:
        elements = []
        if self.name == name:
            elements.append(self)
        if self.children:
            for child in self.children:
                if isinstance(child, HtmlElement):
                    elements.extend(child.get_elements_by_name(name))
        return elements

    def get_elements_by_class_name(self, class_name: str) -> list:
        elements = []
        if "class" in self.attributes and class_name in self.get_attribute("class"):
            elements.append(self)
        if self.children:
            for child in self.children:
                if isinstance(child, HtmlElement):
                    elements.extend(child.get_elements_by_class_name(class_name))
        return elements

    def __str__(self) -> str:
        children_html = ""
        children = self.children or []
        for child in children:
            children_html += child if type(child) is str else str(child)
            children_html += "\n"
        children_html = children_html.strip()
        attributes = (
            json.dumps(self.attributes, separators=(" ", "="))
            .replace("{", " ")
            .replace("}", "")
            .replace("'", "<single_quote>")
            .replace('\\"', "<quote>")
            .replace('"', "")
            .replace("<single_quote>", "'")
            .replace("<quote>", '"')
            .rstrip()
        )
        end = "/>" if children_html == "" else ">"
        block_end = "" if children_html == "" else f"</{self.name}>"
        return f"<{self.name}{attributes}{end}{children_html}{block_end}".strip()

    def _parse(self, html: str):
        html = html.replace("\n", " ")
        element = html_u.get_element(html)
        self.name = html_u.get_name(element)
        self.attributes = html_u.get_attributes(element)
        self.id = self.attributes.get("id")
        if self.id:
            self.id = self.id.replace('"', "")
        children_html = html_u.get_child(html, name=self.name)
        self.children = None
        if children_html is not None:
            self.children = []
            self._add_children(children_html)

    def _add_children(self, html: str):
        if not html:
            return
        try:
            element = html_u.get_element(html)
            name = html_u.get_name(element)
            self.children.append(HtmlElement(html=html, parent=self))
            self._add_children(html_u.remove_element(html, name))
        except AttributeError:
            self.children.append(html)
