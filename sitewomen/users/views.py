from django.http import HttpResponse

def login_user(request):
    return HttpResponse('login')

def logout_user(request):
    return HttpResponse('logout')