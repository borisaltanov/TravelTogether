from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from .forms import TravelForm, TravelSearch
from .models import Travel, TravelRegister
from django.contrib.auth.models import User
from django.http import HttpResponse
from .google import duration, distance
from .calendar import date_time_format, duration_format, travel_export
from .mail import mail_register


@login_required(login_url='/accounts/login/')
def add_travel(request):
    created = False
    context = {}
    form = TravelForm(request.POST or None)
    context['form'] = form
    if form.is_valid():
        travel = form.save(commit=False)
        travel.creator = request.user
        travel.detart_date = form['depart_time']
        travel.start = request.POST.get('start')
        travel.end = request.POST.get('end')
        travel.free_seats = request.POST.get('free_seats')
        travel.fee = request.POST.get('fee')
        travel.duration = duration(travel.start, travel.end)
        print(travel.duration)
        travel.distance = distance(travel.start, travel.end)
        if travel.start == travel.end:
            context['error_message'] = "Start and end must be different"
            return render(request, 'travels/add_travel.html', context)
        travel.save()
        created = True
        context['travel'] = travel
        print (travel.duration)
        print (duration_format(travel.duration))

    context['created'] = created
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

        depart_time = date_time_format(str(travel.depart_time))
        duration = duration_format(travel.duration)
        start = str(travel.start)
        end = str(travel.end)
        user_email = user.email
        username = user.username
        creator = User.objects.get(id=travel.creator_id)

        event_creator = travel_export(
            travel_id, depart_time, duration, start, end, creator.email,
            creator.username, write=True)
        file_name_creator = event_creator[1]

        event_user = travel_export(
            travel_id, depart_time, duration, start, end, user_email,
            username, write=True)
        file_name_user = event_user[1]

        depart_time_regular = str(travel.depart_time)
        mail = mail_register(depart_time_regular, start, end, creator.email,
                             file_name_creator, creator=True)
        mail.send()
        mail = mail_register(
            depart_time_regular, start, end, user_email, file_name_user)
        mail.send()

        return render(request, 'travels/join_success.html',
                      {'travel': travel,
                       'user': user,
                       'travel_reg': travel_reg})


@login_required(login_url='/accounts/login/')
def search_travel(request):
    context = {}
    context = {}
    form = TravelSearch(request.POST or None)
    context['form'] = form
    if form.is_valid():
        start = request.POST.get('start')
        end = request.POST.get('end')
        if start == end:
            context['error_message'] = "Start and end must be different"
            return render(request, 'travels/search.html', context)
        try:
            travels = Travel.objects.filter(
                start=start, end=end).order_by('depart_time')
            context['travels'] = travels
            return render(request, 'travels/search_results.html', context)
        except Travel.DoesNotExist:
            context['error_message'] = "No travels found"
            return render(request, 'travels/search.html', context)

    return render(request, 'travels/search.html', context)


@login_required(login_url='/accounts/login/')
def export_ics(request, travel_id):
    user = request.user
    travel = get_object_or_404(Travel, pk=travel_id)
    if travel:
        depart_time = date_time_format(str(travel.depart_time))
        duration = duration_format(travel.duration)
        start = str(travel.start)
        end = str(travel.end)
        user_email = user.email
        username = user.username

        event = travel_export(
            travel_id, depart_time, duration, start, end, user_email, username)
        file_name = event[1]

        response = HttpResponse(event, content_type="text/calendar")
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            file_name)
        return response
