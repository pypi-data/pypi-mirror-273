from webob import Request


class CustomMiddleware:
    def __init__(self, app):
        self.app = app

    def process_request(self, req):
        pass

    def process_response(self, req, resp):
        pass

    def add(self, middleware_class):
        self.app = middleware_class(self.app)

    def handle_request(self, request):
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)
        return response

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)
