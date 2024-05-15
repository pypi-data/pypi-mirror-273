PY-WEB-FRAMEWORK is a Python web framework build for purposes

![purpose](https://image.shields.io/badge/purpose-learning-green)
![PyPy - Version](https://image.shields.io/pypi/v/pywebframework)


PY-WEB-FRAMEWORK is a Python web framework build for purposes

Installation
```shell
pip install pywebframework-uz
```

Basic usage

```python

from app import PyFrameBuilding
from middleware import CustomMiddleware

server = PyFrameBuilding()


@server.route('/home', allowed_methods=['put', 'post'])
def home(request, response):
    response.status = 200
    response.text = "Hello from Home page"


@server.route('/about')
def about(request, response):
    response.status = 200
    response.text = "Hello from About  page"


@server.route('/about2')
def about2(request, response):
    response.status = 200
    response.text = "Hello from About  page"


@server.route('/hello/{name}')
def greeting(request, response, name):
    response.text = f"Hello {name}"


@server.route('/lessons')
class Lessons:

    def get(self, request, response):
        response.text = "Hello from Lessons class, GET method is called"

    @server.route('/post')
    def post(self, request, response):
        response.text = "Lesson is create, POST method is called"


def new_handler(request, response):
    response.text = 'From new handler'


server.add_route('/new-handler', new_handler


def on_exception(req, resp, exc):
    resp.text = str(exc)


server.add_exception_handler(on_exception)


@server.route('/exception')
def exception_handler(request, response):
    raise AssertionError("Something Bad Happened")


class SimpleMiddleware(CustomMiddleware):


    def process_request(self, req):
        print('The process request came')

    def process_response(self, req, resp):
        print("The response has been generated!")


server.add_middleware(SimpleMiddleware)


```

Unit Tests
The recommended way of writing unit tests is with pytest. There are two built in fixtures that you may want to use when writing unit tests with PYWEBFRAMEWORK.
The first one is app which is an instance of the main API class:

```python

def test_basic_route_adding(app):
    @app.route('/home')
    def home(request, response):
        response.text = "Hello Test"


def test_duplicate_routes_throws_exception(app):
    @app.route('/home')
    def home(request, response):
        response.text = "Hello Test"

    with pytest.raises(AssertionError):
        @app.route('/home')
        def home2(request, response):
            response.text = "Hello Test"
```

The other one is test_client that you can use to send HTTP requests to your handlers. It is based on the famous requests and it should feel very familiar:
```python
def test_alternative_route(app, test_client):
    def new_handler(request, response):
        response.text = 'From new handler'

    app.add_route('/new-handler', new_handler)

    assert test_client.get('http://testserver/new-handler').text == 'From new handler'

```

TEMPLATES

The default folder for templates is 'template'. You can change it when
initializing the  'PyFrameBuilding' class.

```python
@server.route('/template')
def template_handler(request, response):
    response.body = server.template(
        'home.html', context={
            "new_title": 'New Title',
            "new_body": f"Hello 1243"
        }
    )
```


Static files
Just like templates, the default folder for static files is static and you can override it:
server = PyFrameBuilding(static_dir='path/to/static/files/)
```html
<html>
    <header>
        <title>{{new_title}}</title>

        <link rel="stylesheet" href="/static/home.css">
    </header>
    <body>
        {{new_body}}
    </body>

</html>
```