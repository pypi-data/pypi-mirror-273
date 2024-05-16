import re


def get_element(html: str, name: str = "([a-zA-Z][a-zA-Z0-9]*)") -> tuple:
    return re.search(rf"<{name}\b[^>]*>", html).group()


def remove_element(html: str, name: str = "([a-zA-Z][a-zA-Z0-9]*)") -> tuple:
    regex_closed_element_tag = rf"<{name}\b[^\/>]*\/>"
    element = get_element(html, name)
    if re.match(regex_closed_element_tag, element):
        return re.sub(element, "", html, 1)
    children = get_child(html, name=name)
    return (
        html.replace(element, "", 1)
        .replace(children, "", 1)
        .replace(f"</{name}>", "", 1)
        .strip()
    )


def get_name(html: str) -> str:
    return re.search(r"<([a-zA-Z][a-zA-Z0-9]*)\b", html).group().replace("<", "")


def get_attributes(html: str) -> dict:
    attribs = re.search(r"<([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>", html)[2].strip()
    attribs_list = attribs.split(" ")
    attribs_list = _fix_attrs(attribs_list)
    attributes = {}
    last_key = ""
    for attr in attribs_list:
        if attr not in ["", "/"]:
            attr_div = attr.strip().split("=", 1)
            key = attr_div[0]
            if len(attr_div) == 1:
                key = last_key
                value = f"{attributes[key]} {attr_div[0]}"
            else:
                value = attr_div[1]
            last_key = key
            attributes[key] = value
    return attributes


def get_child(html: str, *, name: str) -> str:
    element = get_element(html, name=name)
    if re.match(rf"<{name}\b[^\/>]*\/>", element):
        return None
    children = re.findall(rf"<\/?{name}\b[^>]*>", html)
    children.pop(0)
    element_end = 1
    count = 0
    for element_tag in children:
        if re.match(r"<\/", element_tag):
            element_end -= 1
        else:
            element_end += 1
            count += 1
        if element_end < 1:
            break
    for _ in range(count):
        html = re.sub(rf"<\/{name}>", "<remove>", html, 1)
    (_, start_index) = re.search(rf"<{name}\b[^>]*>", html).span()
    (end_index, _) = re.search(rf"<\/{name}>", html).span()
    html = re.sub("<remove>", f"</{name}>", html)
    end_index = end_index - ((5 - len(name)) * count)
    return html[start_index:end_index].strip()


def _fix_attrs(attrs: list) -> list:
    no_splitable = [",", ":", ";"]
    new_list = []
    mix = None
    for attr in attrs:
        if attr.strip() != "":
            if mix:
                attr = f"{mix} {attr}"
                mix = None
            if attr.strip()[-1] in no_splitable:
                mix = attr
            else:
                new_list.append(attr)
    return new_list
