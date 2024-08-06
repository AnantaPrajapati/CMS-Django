from django.shortcuts import redirect

def AuthMiddleware(get_response):
    def middleware(request):
        protected_paths = []

        if request.path in protected_paths and not request.user.is_authenticated:
            return redirect('api/v1/login')
        
        response = get_response(request)
        return response
    
    return middleware