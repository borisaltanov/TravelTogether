from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import Client
from .models import Account
from .forms import UserForm, AccountForm


class AccountRegister(TestCase):

    def test_register_user_creates_account(self):
        user = User.objects.create_user(username='gosho', email='gosho@abv.bg',
                                        password='proba')
        self.assertEqual(Account.objects.get(user_id=user.id).user_id, user.id)

    def test_account_fields_equal(self):
        user = User.objects.create(
            username='gosho',
            first_name='Gosho',
            last_name='Goshev',
            email='gosho@abv.bg',
            password='probva')
        account = Account.objects.get(user_id=user.id)

        self.assertEqual(account.phone, '+359')

    def test_register_form(self):
        form_data = {
            'username': 'gosho',
            'first_name': 'Gosho',
            'last_name': 'Goshev',
            'email': 'gosho@abv.bg',
            'password1': 'proba',
            'password2': 'proba',
        }
        user_form = UserForm(data=form_data)

        self.assertTrue(user_form.is_valid())

    def test_register_form_error(self):
        form_data = {
            'username': 'gosho',
            'first_name': 'Gosho',
            'last_name': 'Goshev',
            'email': 'gosho@abv.bg',
            'password1': 'proba1',
            'password2': 'proba2',
        }
        user_form = UserForm(data=form_data)

        self.assertFalse(user_form.is_valid())

    def test_account_form(self):
        user = User.objects.create_user(
            username='gosho',
            first_name='Gosho',
            last_name='Goshev',
            email='gosho@abv.bg',
            password='probva')
        form_data = {
            'user': user,
            'phone': '+359888111111',
        }
        account_form = AccountForm(data=form_data)

        self.assertTrue(account_form.is_valid())


class AccountViews(TestCase):

    def test_login(self):
        user = User.objects.create_user(
            username='gosho',
            first_name='Gosho',
            last_name='Goshev',
            email='gosho@abv.bg',
            password='probva')
        client = Client()

        response = client.post('/accounts/login/', {
            'username': user.username,
            'password': 'probva',
        })

        self.assertEqual(response.status_code, 302)

    def test_authenticate(self):
        user = User.objects.create_user(
            username='gosho',
            first_name='Gosho',
            last_name='Goshev',
            email='gosho@abv.bg',
            password='probva')

        response = authenticate(username=user.username, password='probva')

        self.assertTrue(response is not None)

    def test_user_detail(self):
        user = User.objects.create_user(
            username='gosho',
            first_name='Gosho',
            last_name='Goshev',
            email='gosho@abv.bg',
            password='probva'
        )
        client = Client()
        client.post('/accounts/login/', {
            'username': user.username,
            'password': 'probva',
        })
        url = '/accounts/{}/'.format(user.id)
        response2 = client.get(url)
        self.assertEqual(response2.status_code, 200)

    def test_no_user(self):
        user = User.objects.create_user(
            username='gosho',
            first_name='Gosho',
            last_name='Goshev',
            email='gosho@abv.bg',
            password='probva'
        )
        client = Client()
        client.post('/accounts/login/', {
            'username': user.username,
            'password': 'probva',
        })
        url = '/accounts/{}/'.format(user.id + 1)
        response2 = client.get(url)
        self.assertEqual(response2.status_code, 404)
