class PutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'PUT':
            response = self.get_response(request)
            response['Allow'] = 'GET, POST, HEAD, PUT'
            return response
        return self.get_response(request)
# 'app.middleware.PutMiddleware',