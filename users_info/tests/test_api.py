from django.contrib.auth import login
from django.urls import reverse
from rest_framework.test import APITestCase

from users_info.models import UserModel, CityModel


class LoginTestCase(APITestCase):
    def test_login(self):
        user1 = UserModel(login='user1', first_name='user1', last_name='userov1', email='user1@user.com', is_admin=True)
        user1.set_password('user1')
        user1.save()
        user2 = UserModel(login='user2', first_name='user2', last_name='userov2', email='user2@user.com')
        user2.set_password('user2')
        user2.save()
        url = reverse('api_users_control:login')
        responce1 = self.client.post(url, {'username': user1.login, 'password': 'user1'})
        responce2 = self.client.post(url, {'username': user2.email, 'password': 'user2'})
        responce3 = self.client.post(url, {'username': user2.email, 'password': ""})
        responce4 = self.client.post(url, {'username': 'no_name', 'password': "no_name"})
        self.assertEqual(200, responce1.status_code)
        self.assertEqual(200, responce2.status_code)
        self.assertEqual(400, responce3.status_code)
        self.assertEqual(404, responce4.status_code)

    def test_logout(self):
        url = reverse('api_users_control:logout')
        responce1 = self.client.get(url)
        self.assertEqual(200, responce1.status_code)

    def test_users_list(self):
        user1 = UserModel(login='user1', first_name='user1', last_name='userov1', email='user1@user.com')
        user1.set_password('user1')
        user1.save()
        url1 = reverse('api_users_control:login')
        url2 = reverse('api_users_control:users_list')
        responce1 = self.client.get(url2)
        self.assertEqual(403, responce1.status_code)
        self.client.post(url1, {'username': user1.login, 'password': 'user1'})
        responce2 = self.client.get(url2)
        self.assertEqual(200, responce2.status_code)
        self.assertEqual(1, responce2.data.get('meta').get('pagination').get('page'))

    def test_user_current(self):
        user1 = UserModel(login='user1', first_name='user1', last_name='userov1', email='user1@user.com')
        user1.set_password('user1')
        user1.save()
        url1 = reverse('api_users_control:login')
        url2 = reverse('api_users_control:user_current')
        responce1 = self.client.get(url2)
        self.assertEqual(403, responce1.status_code)
        self.client.post(url1, {'username': user1.login, 'password': 'user1'})
        responce2 = self.client.get(url2)
        self.assertEqual(200, responce2.status_code)
        self.assertEqual(user1.login, responce2.data.get('login'))

    def test_user_update(self):
        user1 = UserModel(login='user1', first_name='user1', last_name='userov1', email='user1@user.com')
        user1.set_password('user1')
        user1.save()
        user2 = UserModel(login='user2', first_name='user2', last_name='userov2', email='user2@user.com')
        user2.set_password('user2')
        user2.save()
        url1 = reverse('api_users_control:login')
        url2 = reverse('api_users_control:user_update', args=[user1.pk])
        url3 = reverse('api_users_control:user_update', args=[user2.pk])
        url4 = reverse('api_users_control:user_update', args=[100])
        responce1 = self.client.patch(url2, {'first_name': 'users1'})
        self.assertEqual(403, responce1.status_code)
        self.client.post(url1, {'username': user1.login, 'password': 'user1'})
        responce2 = self.client.patch(url2, {'first_name': 'users1'})
        self.assertEqual(200, responce2.status_code)
        self.assertEqual('users1', responce2.data.get('first_name'))
        responce3 = self.client.patch(url2, {'login': 'users1'})
        self.assertEqual('user1', responce3.data.get('login'))
        responce4 = self.client.patch(url2, {'is_admin': True})
        self.assertEqual(False, responce4.data.get('is_admin'))
        responce5 = self.client.patch(url3, {'first_name': 'users1'})
        self.assertEqual(403, responce5.status_code)
        responce6 = self.client.patch(url4, {'first_name': 'users1'})
        self.assertEqual(403, responce6.status_code)

    def test_private_users_list_create(self):
        city1 = CityModel(name="Moscow")
        city1.save()
        user1 = UserModel(login='user1', first_name='user1', last_name='userov1', email='user1@user.com', city=city1)
        user1.set_password('user1')
        user1.save()
        user2 = UserModel(login='user2', first_name='user2', last_name='userov2', email='user2@user.com', is_admin=True)
        user2.set_password('user2')
        user2.save()
        url1 = reverse('api_users_control:login')
        url2 = reverse('api_users_control:private_users_list_create')
        responce1 = self.client.get(url2)
        self.assertEqual(403, responce1.status_code)
        self.client.post(url1, {'username': user1.login, 'password': 'user1'})
        responce2 = self.client.get(url2)
        self.assertEqual(403, responce2.status_code)
        self.client.post(url1, {'username': user2.login, 'password': 'user2'})
        responce3 = self.client.get(url2)
        self.assertEqual(200, responce3.status_code)
        self.assertEqual((1, 'Moscow'), responce3.data.get('meta').get('hint').get('city')[0])
        responce4 = self.client.post(url2, {'login': 'login', 'first_name': 'first_name', 'last_name': 'last_name',
                                            'email': 'email@mail.com', 'password': 'password', 'is_admin': True})
        self.assertEqual(201, responce4.status_code)
        responce5 = self.client.post(url2, {'login': 'login2', 'first_name': 'first_name',
                                            'email': 'email@mail2.com', 'password': 'password', 'is_admin': True})
        self.assertEqual(400, responce5.status_code)
        responce6 = self.client.post(url2, {'login': 'login3', 'first_name': 'first_name', 'last_name': 'last_name',
                                            'email': 'email', 'password': 'password'})
        self.assertEqual(400, responce6.status_code)
        responce7 = self.client.post(url2, {'login': 'login', 'first_name': 'first_name', 'last_name': 'last_name',
                                            'email': 'email@mail.com', 'password': 'password'})
        self.assertEqual(400, responce7.status_code)
        responce8 = self.client.post(url2, {'login': 'login4', 'first_name': 'first_name', 'last_name': 'last_name',
                                            'email': 'email@mail4.com', 'password': 'password', 'city': 1})
        self.assertEqual(201, responce8.status_code)
        url2 = reverse('api_users_control:private_users_list_create')
        responce9 = self.client.post(url2, {'login': 'login5', 'first_name': 'first_name', 'last_name': 'last_name',
                                            'email': 'email@mail5.com', 'password': 'password', 'city': 135})
        self.assertEqual(400, responce9.status_code)
        responce10 = self.client.get(url2+'?search=login4')
        self.assertEqual('login4', responce10.data.get('data')[0].get('login'))

    def test_private_user_edit(self):
        city1 = CityModel(name="Moscow")
        city1.save()
        user1 = UserModel(login='user1', first_name='user1', last_name='userov1', email='user1@user.com', city=city1)
        user1.set_password('user1')
        user1.save()
        user2 = UserModel(login='user2', first_name='user2', last_name='userov2', email='user2@user.com', is_admin=True)
        user2.set_password('user2')
        user2.save()
        url1 = reverse('api_users_control:login')
        url2 = reverse('api_users_control:private_user_edit', args=[user1.pk])
        responce1 = self.client.get(url2)
        self.assertEqual(403, responce1.status_code)
        self.client.post(url1, {'username': user1.login, 'password': 'user1'})
        responce2 = self.client.get(url2)
        self.assertEqual(403, responce2.status_code)
        self.client.post(url1, {'username': user2.login, 'password': 'user2'})
        responce3 = self.client.get(url2)
        self.assertEqual(200, responce3.status_code)
        self.assertEqual('user1', responce3.data.get('login'))
        responce4 = self.client.patch(url2, {'login': 'login'})
        self.assertEqual(200, responce4.status_code)
        self.assertEqual('login', responce4.data.get('login'))
        responce5 = self.client.patch(url2, {'id': 100})
        self.assertEqual(1, responce5.data.get('id'))
        responce6 = self.client.delete(url2)
        self.assertEqual(204, responce6.status_code)
        responce7 = self.client.get(url2)
        self.assertEqual(404, responce7.status_code)




