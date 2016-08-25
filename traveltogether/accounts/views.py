from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from travels.models import Travel
from .forms import UserForm, AccountForm
from django.contrib import messages


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        account_form = AccountForm(data=request.POST)

        if user_form.is_valid() and account_form.is_valid():
            print(user_form.is_valid())
            # save user
            user = user_form.save()
            # set account's user and save
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            registered = True
            messages.success(request, 'You have been registered')

        else:
            print (user_form.errors, account_form.errors)

    else:
        user_form = UserForm()
        account_form = AccountForm()

    return render(request,
                  'accounts/register.html',
                  {'user_form': user_form,
                   'account_form': account_form,
                   'messages': messages,
                   'registered': registered})


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                print(type(user))
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            # invalid user print
            print ("Invalid login details: {0}, {1}".format(
                username, password))
            return HttpResponse("Invalid login details supplied.")
    else:

        return render(request, 'accounts/login.html', {})


@login_required(login_url='/accounts/login/')
def user_logout(request):
    logout(request)
    # back to homepage
    return HttpResponseRedirect('/')


@login_required(login_url='/accounts/login/')
def details(request, account_id):
    user = User.objects.get(id=account_id)
    travels = Travel.objects.filter(creator_id=account_id)

    return render(request, 'accounts/details.html',
                  {'user': user, 'travels': travels})
