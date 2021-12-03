from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status

from .base import BaseTestClass
from .factories.category_factory import CategoryFactory


class BaseCategoryTest(BaseTestClass):
    @staticmethod
    def create_category(owner):
        return CategoryFactory(owner=owner)


class CreateCategoryTests(BaseCategoryTest):
    """
    Class provides testing creating category.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("api:summary:category-list")
        cls.new_category = model_to_dict(
            CategoryFactory.build(),
            fields=('type', 'title'),
        )

    def test_right_auth_header(self):
        """
        Test that request has right http header authorization.
        Response must have 201 status code.
        """
        response = self.client.post(path=self.url, data=self.new_category)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_auth_header(self):
        """
        Test that request with `bad` http header authorization don't work.
        Response must have 401 status code.
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(path=self.url, data=self.new_category)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListCategoryTests(BaseCategoryTest):
    """
    Class provides testing getting list of categories.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("api:summary:category-list")

        # create own category
        cls.create_category(cls.user)
        # create someone else's category
        cls.create_category(cls.another_user)

    def test_get_only_personal_categories(self):
        """
        Check that user will get only personal categories.
        Test assumes that exist category[-ies] owned by different user[-s].
        """
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for category in response.data:
            self.assertEqual(category['owner'], self.user.id)


class DeleteCategoryTests(BaseCategoryTest):
    """
    Class provides testing deleting category.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # create own category
        cls.own_category = cls.create_category(cls.user)
        # create someone else's category
        cls.another_category = cls.create_category(cls.another_user)

    def test_delete_own_category(self):
        """
        Test that user can delete own category.
        """
        url = reverse(
            "api:summary:category-detail", args=[self.own_category.id]
        )
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_category(self):
        """
        Test that user can't delete someone else's category.
        """
        url = reverse(
            "api:summary:category-detail", args=[self.another_category.id]
        )
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
