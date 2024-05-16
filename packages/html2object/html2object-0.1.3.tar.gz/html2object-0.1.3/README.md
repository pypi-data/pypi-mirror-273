[![Coverage Status](https://coveralls.io/repos/github/boterop/html2object/badge.svg?branch=main)](https://coveralls.io/github/boterop/html2object?branch=main)

# HTML 2 Object

Tools to handle the CRUD of .html files as objects.

## Install

```sh
pip install html2object
```

## Usage

This project provides a way to manipulate HTML files and update them dynamically. Here's how you can use it:

First, import the necessary classes from this project:

```sh
from html2object import HtmlElement
```

read your html file and create an `HtmlElement()`

```sh
html = open(<path>, "r").read("bin/gui/index.html")
document = HtmlElement(html)
```

now you can create scripts

```sh
update_script = HtmlElement(name="script").add_child(
    "setInterval(() => reload(), 1500);"
)
document.add_child(update_script)
```

create a div

```sh
p = HtmlElement(name="p", id="textID").add_chil("Text")
div = HtmlElement(name="div").add_child(p)
document.add_child(div)
```

or even find an element

```sh
text_element = document.find_element_by_id("textID")
strong = HtmlElement(name="strong").add_child("Strong text")
text_element.set_child([strong, "No strong text"])
```

save the html file running

```sh
open(path, "w").write(str(document)).close()
```

## Local setup

Instructions on how to install and set up your project. Include any dependencies that need to be installed.

1. Clone the repository
2. Navigate to the project directory:

```sh
cd html2object
```

3. Create a virtual environment (optional but recommended):

```sh
python3 -m venv venv
```

4. Activate the virtual environment:

- For Windows:

```sh
venv\Scripts\activate
```

- For macOS and Linux:

```sh
source venv/bin/activate
```

5. Install the project dependencies:

```sh
pip install -r requirements.txt
```

That's it! Your project should now be installed and ready to use.
