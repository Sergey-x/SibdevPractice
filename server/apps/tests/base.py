from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories.custom_user_factory import CustomUserFactory


class BaseTestClass(APITestCase):
    """
    Base class for testing apps.
    """

    @classmethod
    def setUpTestData(cls):
        # create main user
        cls.user = CustomUserFactory()
        cls.another_user = CustomUserFactory()

    def get_access_token(self, user):
        credentials = {
            "email": user.email,
            "password": user.username,
        }
        url = reverse('api:token_obtain_pair')
        response = self.client.post(path=url, data=credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def setUp(self) -> None:
        """
        Add Authentication: "Bearer `access_token`"
        """
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.get_access_token(self.user)}"
        )
