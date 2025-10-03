![PyServeUz Logo](pyserve.jpg)


# PyServeUz : Python Web Framework built for learning purposes

![build](https://badgen.net/badge/purpose-learning/passing/green?icon=github)

[![PyPI version](https://badgen.net/pypi/v/requests)](https://pypi.org/project/requests/)


PyServeUz is a lightweight Python web framework created for learning and experimentation.  It follows the WSGI standard and works seamlessly with any WSGI application server such as Gunicorn or uWSGI.


## Installation

```shell
pip install pyserveuz
```

## How to use it

### Basic usage:

```python
from pyserveuz.app import PyServeApp

app = PyServeApp()

@app.route("/home",allowed_methods = ["get"])
def home(request,response):
    response.text = "Hello from the Home Page"

    
@app.route("/hello/{name}")
def greeting(request,response,name):
    response.text = f"Hello {name}"


@app.route("/books")
class BooksRecourse:
    def get(self,request,response):
        response.text = "Books page"
    
    def post(self,request,response):
        response.text = "Endpoint to create a book"


        
    
@app.route("/template")
def template_handler(req,resp):
    resp.html = app.template(
        "home.html",
        context = {
            "new_title":"new title",
            "new_body":"hi bro"
        }
    )


@app.route("/json")
def json_handler(req,resp):
    response_data = {"name":"john","type":"json"}
    resp.json = response_data
```


### Unit tests

The recommended way to write unit tests in PyServeUz is by using [pytest](https://docs.pytest.org/en/latest/).PyServeUz provides two built-in fixtures that simplify testing your applications.  The first one is `app`, which represents an instance of the main `PyServeApp` class. 


```python

def test_duplicate_routes_throws_exception(app):
    @app.route("/home")
    def home(req,resp):
        resp.text = "Hello from home"
        
    with pytest.raises(AssertionError):
        @app.route("/home")
        def home2(req,resp):
            resp.text = "Hello from home2"
```
The other one is `client`, which you can use to send HTTP requests to your handlers.  It is built on top of the popular [requests](https://requests.readthedocs.io/) library,  so the API should feel very familiar if you have used `requests` before.  With the `client` fixture, you can easily test endpoints by sending GET, POST, or other HTTP requests and then asserting the responses in your unit tests.


```python
def test_parameterized_routing(app,test_client):
    @app.route("/hello/{name}")
    def greeting(request,response,name):
        response.text = f"Hello {name}"
    
    assert test_client.get("http://testserver/hello/Tom").text == "Hello Tom"
    assert test_client.get("http://testserver/hello/Matthew").text == "Hello Matthew"
```


## Templates

The default folder for templates is 'templates'. You can change it when initialializing the main 'API()' class : 


```python 
app = PyServeApp(templates_dir = "templates_dir_name")
```

Then you can use HTML files in that folder like so in a handler:

```python
@app.route("/show/template")
def template_handler(req,resp):
    resp.html = app.template(
        "home.html",
        context = {
            "new_title":"new title",
            "new_body":"hi bro"
        }
    )
```


## Static Files 

Just like templates, the default folder for static files is 'static' and you can override it:

```python
app = API(static_dir="static_dir_name")
```

Then you can use the files inside this folder in HTML files:

```html
<!DOCTYPE html>
<html>
    <head>
    <title>{{new_title}}</title>
    <link rel="stylesheet" href="static/home.css">
    </head>

    <body>
        {{new_body}}
    </body>

</html>
```

### Middleware 

PyServeUz provides a simple middleware system that lets you run custom logic
before and after each request. 

```python
from pyserveuz.app import PyServeApp
from pyserveuz.middleware import Middleware

app = PyServeApp()


class LoggingMiddleware(Middleware):
    def process_request(self, req):
        print("request is being called")
    
    def process_response(self, req, resp):
        print("response has been generated")

app.add_middleware(LoggingMiddleware)

```

## Features

- WSGI compatible
- Parameterized and basic routing
- Class based handlers
- Test Client
- Support for templates
- Support for static files
- Custom exception handler
- Middleware