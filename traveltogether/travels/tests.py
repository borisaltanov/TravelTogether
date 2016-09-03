from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
from .models import Travel


class TestTravel(TestCase):

    def test_create_travel(self):
        user = User.objects.create_user(
            username='gosho',
            first_name='Gosho',
            last_name='Goshev',
            email='gosho@abv.bg',
            password='probva'
        )

        travel = Travel.objects.create(
            creator=user,
            depart_time=timezone.localtime(timezone.now()),
            start='София',
            end='Варна',
            free_seats=4,
            fee=10,
            duration='5 hours 19 mins',
            distance='494 km',
        )

        self.assertTrue(travel is not None)

    def test_access_travel_logged_in(self):
        user = User.objects.create_user(
            username='gosho',
            first_name='Gosho',
            last_name='Goshev',
            email='gosho@abv.bg',
            password='probva',
        )

        travel = Travel.objects.create(
            creator=user,
            depart_time=timezone.localtime(timezone.now()),
            start='София',
            end='Варна',
            free_seats=4,
            fee=10,
            duration='5 hours 19 mins',
            distance='494 km',
        )

        client = Client()
        client.post('/accounts/login/', {
            'username': user.username,
            'password': 'probva',
        })

        url = '/travels/{}/'.format(travel.id)
        access = client.get(url)

        self.assertEqual(access.status_code, 200)
