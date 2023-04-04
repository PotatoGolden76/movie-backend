from django.urls import resolve, reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
# from movies_api import *


class APITests(APITestCase):
    actorStatURL = reverse('stat')
    ratingStatURL = reverse('rating')

    def test_stat(self):
        self.assertEqual(resolve(self.actorStatURL).route, "api/movies/stat")

    def test_rating(self):
        self.assertEqual(resolve(self.ratingStatURL).route, "api/movies/rating")

    def test_get_stat(self):
        response = self.client.get(self.actorStatURL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rating(self):
        response = self.client.get(self.ratingStatURL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
