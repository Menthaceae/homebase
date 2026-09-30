from django.shortcuts import render


def layout(request):
    return render(request, 'layout.html')
# GET /
def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')