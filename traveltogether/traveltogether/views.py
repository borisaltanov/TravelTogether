from django.shortcuts import render


def index(request):
    user = request.user
    return render(request,
                  'base.html', {'user': user})
