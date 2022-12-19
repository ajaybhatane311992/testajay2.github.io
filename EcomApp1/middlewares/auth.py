from django.shortcuts import redirect
def auth_middleware(get_response):  #write Custom Name
    def middleware(request):
        return_url=request.META['PATH_INFO']
        if not request.session.get('cid'):
            return redirect(f'/ecom/login/?return_url={return_url}')
        response = get_response(request)
        return response
    return middleware