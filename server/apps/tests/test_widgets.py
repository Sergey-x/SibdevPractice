from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status

from .base import BaseTestClass
from .factories.category_factory import CategoryFactory
from .factories.widget_factory import WidgetFactory


class BaseWidgetTests(BaseTestClass):
    """
    Base class for testing widget functionalities.
    """

    @staticmethod
    def create_widget(owner):
        return WidgetFactory(
            owner=owner,
            category=CategoryFactory(owner=owner),
        )


class CreateWidgetTests(BaseWidgetTests):
    """
    Class provides testing creating widget.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.url = reverse("api:widgets:widgets-list")

        created_widget = WidgetFactory.build()
        created_widget.category = CategoryFactory(owner=cls.user)
        cls.new_widget = model_to_dict(created_widget, exclude=('id', 'owner'))

    def test_right_auth_header(self):
        """
        Test that request has right http header authorization.
        Response must have 201 status code.
        """
        response = self.client.post(path=self.url, data=self.new_widget)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_auth_header(self):
        """
        Test that request with `bad` http header authorization don't work.
        Response must have 401 status code.
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(path=self.url, data=self.new_widget)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListWidgetTests(BaseWidgetTests):
    """
    Class provides testing getting list of widgets.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("api:widgets:widgets-list")
        # create own widget
        cls.create_widget(owner=cls.user)
        # create someone else's widget
        cls.create_widget(owner=cls.another_user)

    def test_get_only_personal_widgets(self):
        """
        Check that user will get only personal widgets.
        Test assumes that exist widgets owned by different users.
        """
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for widget in response.data:
            self.assertEqual(widget['owner'], self.user.id)


class DeleteWidgetTests(BaseWidgetTests):
    """
    Class provides testing deleting widget.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # create own widget
        cls.own_widget = cls.create_widget(cls.user)
        # create someone else's widget
        cls.another_widget = cls.create_widget(cls.another_user)

    def test_delete_own_widget(self):
        """
        Test that user can delete own widget.
        """
        url = reverse("api:widgets:widgets-detail", args=[self.own_widget.id])
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_widget(self):
        """
        Test that user can't delete someone else's widget.
        """
        url = reverse(
            "api:widgets:widgets-detail", args=[self.another_widget.id]
        )
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
