class LikeFlask:
    def __call__(self, environ: dict, start_response) -> list:
        """Main WSGI function"""

        # Request parsing
        self.path: str = environ['PATH_INFO']
        self.method: str = environ['REQUEST_METHOD']
        self.protocol: str = environ['SERVER_PROTOCOL']

        # Get response from particular handler
        responses = list()
        for handler in self.views:
            responses.append(handler())

        # Check if response have any data
        response = [i for i in responses if i is not None]
        if response:
            status, headers, body = response[0]
        else:
            status, headers, body = self.page_not_found()

        # Send data to the client
        start_response(status, headers)
        return [body]

    def route(self, path, methods=['GET']):
        def decorator(func):
            def wrapper() -> tuple | None:
                if self.path == path:  # Func comparison
                    if self.method in methods:
                        status = '200 OK'
                        headers = [('Content-type', 'text/html')]
                        body = func()
                    else:
                        status = '405 Method Not Allowed'
                        headers = [('Content-type', 'text/html')]
                        body = "<h1>Method not allowed<h1>"

                    return status, headers, body
                else:
                    return None
            return wrapper
        return decorator

    def page_not_found(self):
        status = '404 Not Found'
        headers = [('Content-type', 'text/html')]
        body = "<h1>Page not found<h1>"

        return status, headers, body


app = LikeFlask()


@app.route('/')
def index():
    return "<h1>Main page</h1>"


@app.route('/about')
def about():
    return "<h1>About</h1>"


app.views = [obj for obj in vars().values() if hasattr(obj, '__class__') and obj.__class__.__name__ == 'function']
