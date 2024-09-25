from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Item


class ItemViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.item = Item.objects.create(name="Test Item", description="Test description")

    def test_create_item(self):
        """ Test for creating a new item (Success Case) """
        data = {'name': 'New Item', 'description': 'New description'}
        response = self.client.post(reverse('item-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Item')

    def test_create_existing_item(self):
        """ Test for creating an item that already exists (Error Case) """
        data = {'name': 'Test Item', 'description': 'Duplicate description'}
        response = self.client.post(reverse('item-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('name', response.data)  

        self.assertIn('item with this name already exists.', str(response.data['name'][0]))


    def test_list_items(self):
        """ Test for listing all items """
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Item.objects.count())

    def test_retrieve_item(self):
        """ Test for retrieving a single item by id """
        response = self.client.get(reverse('item-detail', kwargs={'pk': self.item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_retrieve_non_existing_item(self):
        """ Test for retrieving an item that does not exist (Error Case) """
        response = self.client.get(reverse('item-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        """ Test for updating an existing item """
        data = {'name': 'Updated Item', 'description': 'Updated description'}
        response = self.client.put(reverse('item-detail', kwargs={'pk': self.item.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Item')

    def test_delete_item(self):
        """ Test for deleting an existing item """
        response = self.client.delete(reverse('item-detail', kwargs={'pk': self.item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_non_existing_item(self):
        """ Test for deleting an item that does not exist (Error Case) """
        response = self.client.delete(reverse('item-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_token_obtain_pair(self):
        """ Test for obtaining JWT access and refresh tokens """
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(reverse('token_obtain_pair'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """ Test for refreshing JWT access token """
        refresh = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh)}
        response = self.client.post(reverse('token_refresh'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
