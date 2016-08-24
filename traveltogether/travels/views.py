from django.shortcuts import render
#from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import TravelForm
from .models import Travel, TravelRegister
from django.contrib.auth.models import User
# Create your views here.


@login_required(login_url='/accounts/login/')
def add_travel(request):
    form = TravelForm(request.POST or None)
    if form.is_valid():
        travel = form.save(commit=False)
        travel.creator = request.user
        travel.detart_date = form['depart_time']
        travel.start = request.POST.get('start')
        travel.end = request.POST.get('end')
        travel.free_seats = request.POST.get('free_seats')
        travel.fee = request.POST.get('fee')
        if travel.start == travel.end:
            context = {
                'travel': travel,
                'form': form,
                'error_message': 'Start and end must be different',
            }
            return render(request, 'travels/add_travel.html', context)
        travel.save()
        return render(request, 'travels/detail.html', {'travel': travel})

    context = {
        "form": form,
    }
    return render(request, 'travels/add_travel.html', context)


@login_required(login_url='/accounts/login/')
def detail(request, travel_id):
    user = request.user
    travel = get_object_or_404(Travel, pk=travel_id)
    reg_users = TravelRegister.objects.filter(travel_id=travel_id)
    ids = [reg_user.user_id for reg_user in reg_users]
    users = User.objects.filter(id__in=ids)
    is_creator = False
    seats_check = False
    travel_registered = False
    try:
        travel_registered = TravelRegister.objects.get(
            travel_id=travel_id, user_id=request.user.id)
    except TravelRegister.DoesNotExist:
        pass
    if travel.creator_id == user.id:
        is_creator = True
    if travel.free_seats == 0:
        seats_check = True
    return render(request, 'travels/detail.html',
                  {'travel': travel,
                   'user': user,
                   'users': users,
                   'is_creator': is_creator,
                   'seats_check': seats_check,
                   'travel_registered': travel_registered,
                   })


@login_required(login_url='/accounts/login/')
def index(request):
    travels = Travel.objects.all()
    return render(
        request, 'travels/index.html', {'travels': travels, })


@login_required(login_url='/accounts/login/')
def join_travel(request, travel_id):
    user = request.user
    travel = get_object_or_404(Travel, pk=travel_id)
    if travel.free_seats >= 1:
        travel.free_seats -= 1
        travel.save()
        travel_reg = TravelRegister(user=user, travel=travel)
        travel_reg.save()

        return render(request, 'travels/join_success.html',
                      {'travel': travel,
                       'user': user,
                       'travel_reg': travel_reg})
