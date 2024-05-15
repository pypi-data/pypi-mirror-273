# Attributes

| dj-assets      | Modify the "href" or "src" attributes of elements with a path prefix and wrap them in a Django static command. |
|----------------|----------------------------------------------------------------------------------------------------------------|
| Syntax         | `<html dj-assets="asset_identifier;asset_prefix">...</html>`                                                   |
| Example Input  | `<html dj-assets="assets;module"><img src="assets/image.png"></html>`                                          |
| Example Output | `<html><img src="{% static 'module/assets/image.png' %}"/></html>`                                             |

| dj-attr        | Dynamically assign attributes using Django template variables.                        |
|----------------|---------------------------------------------------------------------------------------|
| Syntax         | `<element dj-attr="attribute1;value1~attribute2;value2~attribute3;value3"></element>` |
| Example Input  | `<div dj-attr="class;my-class~id;my-id"></div>`                                       |
| Example Output | `<div class="{{ my-class }}" id="{{ my-id }}"></div>`                                 |

| dj-block       | Replace the element with Django block tags.         |
|----------------|-----------------------------------------------------|
| Syntax         | `<element dj-block="blockname">Content</element>`   |
| Example Input  | `<div dj-block="content">Content</div>`             |
| Example Output | `{% block content %}Content{% endblock %}`          |

| dj-command     | Replace the element with a Django template command.         |
|----------------|-------------------------------------------------------------|
| Syntax         | `<element dj-command="command"></element>`                  |
| Example Input  | `<div dj-command="url 'index'"></div>`                      |
| Example Output | `{% url 'index' %}`                                         |

| dj-for         | Replace the element with a Django template for loop.         |
|----------------|--------------------------------------------------------------|
| Syntax         | `<element dj-for="item in list">Content</element>`           |
| Example Input  | `<div dj-for="item in list"><p>Hello</p></div>`              |
| Example Output | `{% for item in list %}<p>Hello</p>{% endfor %}`             |

| dj-for-wrap    | Wrap the element within a Django template for loop.         |
|----------------|-------------------------------------------------------------|
| Syntax         | `<element dj-for-wrap="item in list">Content</element>`     |
| Example Input  | `<div dj-for-wrap="item in list">Content</div>`             |
| Example Output | `{% for item in list %}<div>Content</div>{% endfor %}`      |

| dj-if, dj-elif, dj-else | Replace the elements with a Django template if-elif-else structure.                                                                                      |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Syntax                  | `<element dj-if="condition">Content</element>`<br/>`<element dj-elif="condition">Content</element>`<br/>`<element dj-else="condition">Content</element>` |
| Note                    | The `dj-elif` and `dj-else` attributes are optional. Multiple `dj-elif` attributes are allowed.                                                          |
| Example Input           | `<div dj-if="condition1">Test</div><div dj-elif="condition2">Test2</div><div dj-else>Test3</div>`                                                        |
| Example Output          | `{% if condition1 %}Test{% elif condition2 %}Test2{% else %}Test3{% endif %}`                                                                            |

| dj-include     | Replace the content of the element with a Django template include command. |
|----------------|----------------------------------------------------------------------------|
| Syntax         | `<element dj-include="template_name"></element>`                           |
| Example Input  | `<div dj-include="template_name.html"></div>`                              |
| Example Output | `{% include "template_name.html" %}`                                       |

| dj-remove-default | Remove the Doctype, "head" element, and "script" element within the "body" element. It also unwraps the "body" and "html" elements, leaving only the remaining content of the "body" element. |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Syntax            | `<html dj-remove-default>...</html>`                                                                                                                                                          |
| Note              | This is meant to remove all the default html wrapper code most static html generators produce.                                                                                                |
| Example Input     | `<!DOCTYPE html><html dj-remove-default><head>...</head><body>Content<script>...</script></body></html>`                                                                                      |
| Example Output    | `Content`                                                                                                                                                                                     |

| dj-remove      | Remove the element.             |
|----------------|---------------------------------|
| Syntax         | `<element dj-remove></element>` |
| Example Input  | `<div><p dj-remove></p></div>`  |
| Example Output | ` `                             |

| dj-static      | Replace the value of the specified tag with a Django template static command, using the specified static file path. |
|----------------|---------------------------------------------------------------------------------------------------------------------|
| Syntax         | `<element dj-static="tag;static_file_path"></element>`                                                              |
| Example Input  | `<img dj-static="src;images/pic.jpg">`                                                                              |
| Example Output | `<img src="{% static 'images/pic.jpg' %}"/>`                                                                        |

| dj-style       | Modify the style attribute of a element with django variables.                             |
|----------------|--------------------------------------------------------------------------------------------|
| Syntax         | `<element dj-style="property1;value1;value_type1~property2;value2;value_type2"></element>` |
| Note           | The `value_type` is optional. If not included still add the `;` after the value.           |
| Example Input  | `<div style="color:red" dj-style="background-color;color;~padding;padding;px">`            |
| Example Output | `<div style="color:red;background-color:{{ color }};padding:{{ padding }}px">`             |

| dj-style-raw   | Modify the style attribute of a element. The value will be inserted as is.       |
|----------------|----------------------------------------------------------------------------------|
| Syntax         | `<element dj-style-raw="property1;value1~property2;value2"></element>`           |
| Example Input  | `<div style="color:red" dj-style-raw="background-color;blue~color:{{ color }}">` |
| Example Output | `<div style="color:{{ color }};background-color:blue">`                          |

| dj-unwrap      | Remove the element's tags but keeps its content. |
|----------------|--------------------------------------------------|
| Syntax         | `<element dj-unwrap>Content</element>`           |
| Example Input  | `<div dj-unwrap><p>Hello, world!</p></div>`      |
| Example Output | `<p>Hello, world!</p>`                           |

| dj-var         | Replace the element's content with a Django template variable. |
|----------------|----------------------------------------------------------------|
| Syntax         | `<element dj-var="variable_name">Content</element>`            |
| Example Input  | `<p dj-var="greeting">Hello, world!</p>`                       |
| Example Output | `<p>{{ greeting }}</p>`                                        |