class ViewNameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add the view name to request.META
        temp = request.resolver_match
        if temp:
            request.META['VIEW_NAME'] = request.resolver_match.view_name
        request.META['VIEW_NAME'] = None

        response = self.get_response(request)
        return response
